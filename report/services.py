from django.core.cache import cache
import json
import time
from wemark.commons.services import BatchService, ProductService, DataService
from wemark.commons import constants


class ReportService(object):
    CACHE_EXPIRES_IN = constants.TIME_SECOND_UNIT
    BATCH_CACHE_KEY = 'batch_cache_key'
    SCAN_CODE_CACHE_KEY = 'scan_code_cache_key_of_'
    AWARD_CACHE_KEY = 'award_code_cache_key_of_'

    def __init__(self, user_id, is_root=False):
        super(ReportService, self).__init__()
        self.is_root = is_root
        self.user_id = user_id

    def __get_batch_list(self):
        batch_list = cache.get(self.__generate_key(self.BATCH_CACHE_KEY))
        if batch_list is not None:
            return batch_list

        batch_list = BatchService.get_batch_list(status=constants.BatchStatus.Done)['data'] if self.is_root \
            else BatchService.get_batch_list(created_by=self.user_id, status=constants.BatchStatus.Done)['data']
        cache.set(self.__generate_key(self.BATCH_CACHE_KEY), batch_list, self.CACHE_EXPIRES_IN)

        return batch_list

    def __get_scan_list(self, bid, user_type):
        scan_list = cache.get(self.__generate_key(self.SCAN_CODE_CACHE_KEY, bid))
        if scan_list is None:
            if bid in self.get_batches_ids():
                scan_list = DataService.get_scan_code_list(batch_id=bid, user_type=user_type)['data']
                cache.set(self.__generate_key(self.SCAN_CODE_CACHE_KEY, bid), scan_list, self.CACHE_EXPIRES_IN)
        return scan_list

    def __get_accepted_list(self, bid, user_type):
        accepted_list = cache.get(self.__generate_key(self.AWARD_CACHE_KEY, bid))
        if accepted_list is None:
            if bid in self.get_batches_ids():
                accepted_list = DataService.get_award_list(batch_id=bid, user_type=user_type)['data']
                cache.set(self.__generate_key(self.AWARD_CACHE_KEY, bid), accepted_list, self.CACHE_EXPIRES_IN)
        return accepted_list

    @staticmethod
    def __get_batch(bid):
        return BatchService.get_batch(bid)['data']

    def __get_product_by_barcode(self, barcode):
        products = ProductService.get_product_list(barcode=barcode)['data'] \
            if self.is_root else ProductService.get_product_list(barcode=barcode, created_by=self.user_id)['data']
        return products[0] if len(products) != 0 else None

    @staticmethod
    def __generate_key(prefix, ordinal=None):
        return prefix + str(ordinal) if ordinal is not None else prefix

    def get_batches_ids(self):
        return [item['id'] for item in self.__get_batch_list()]

    def get_total_scan_count(self, bid, user_type=constants.UserType.Wechat):
        scan_list = self.__get_scan_list(bid, user_type)
        ret = 0
        if scan_list is not None:
            for scan_code in scan_list:
                ret += scan_code['scanTimes']
        return ret

    def get_total_code_count(self, bid):
        if bid in self.get_batches_ids():
            json_obj = DataService.get_associated_code_count(bid)
            return json_obj['data'] if json_obj['code'] == 0 else 0
        return 0

    @staticmethod
    def get_total_award_amount():
        default_award_amount = 5000000
        return default_award_amount

    def get_total_accepted_count(self, bid, user_type=constants.UserType.Wechat):
        accepted_list = self.__get_accepted_list(bid, user_type)
        return len(accepted_list) if accepted_list is not None else 0

    def get_total_accepted_amount(self, bid, user_type=constants.UserType.Wechat):
        accepted_list = self.__get_accepted_list(bid, user_type)
        ret = 0
        if accepted_list is not None:
            for accept in accepted_list:
                info = json.loads(accept['awardInfo']) if accept['awardInfo'] else None
                ret += float(info['amount']) / constants.UNIT_CHINA_FEN \
                    if info is not None and info['amount'] is not None else 0
        return ret

    def get_daily_scan_and_accepted_count(self, bid, user_type=constants.UserType.Wechat):
        def create_daily_item(date_str, scan, confirm):
            return {
                'date': date_str,
                'scan': scan,
                'confirm': confirm
            }

        def format_timestamp(timestamp_in_second):
            t = time.localtime(timestamp_in_second)
            return time.strftime("%Y-%m-%d", t)

        date_map = {}
        now = time.time()
        current = now
        days_for_display = 15
        for d in xrange(days_for_display):
            date_map[format_timestamp(current)] = [0, 0]
            current -= constants.TIME_HOUR_UNIT * constants.TIME_MINUTE_UNIT * constants.TIME_SECOND_UNIT

        scan_list = self.__get_scan_list(bid, user_type)
        accepted_list = self.__get_accepted_list(bid, user_type)
        if scan_list is not None:
            for scan_code in scan_list:
                ts_in_millis = scan_code['scanTime']
                times = scan_code['scanTimes']
                date = format_timestamp(ts_in_millis / constants.TIME_MILLIS_UNIT)
                if date_map[date] is not None:
                    date_map[date][0] += times
        if accepted_list is not None:
            for accepted in accepted_list:
                ts_in_millis = accepted['awardAcptTime']
                date = format_timestamp(ts_in_millis / constants.TIME_MILLIS_UNIT)
                if date_map[date] is not None:
                    date_map[date][1] += 1

        ret = []
        current = now
        for d in xrange(days_for_display):
            date = format_timestamp(current)
            ret.append(create_daily_item(date, date_map[date][0], date_map[date][1]))
            current -= constants.TIME_HOUR_UNIT * constants.TIME_MINUTE_UNIT * constants.TIME_SECOND_UNIT
        ret.reverse()

        return ret

    def get_accepted_rate_by_product(self):
        def create_product_item(product_name, rate):
            return {
                'category': product_name,
                'rate': rate
            }

        product_map = {}
        batch_list = self.__get_batch_list()
        if batch_list is not None:
            for batch in batch_list:
                barcode = batch['barcode']
                product = self.__get_product_by_barcode(barcode)
                if product is not None:
                    name = product['name']
                    scan_count = self.get_total_scan_count(batch['id'])
                    accepted_count = self.get_total_accepted_count(batch['id'])
                    if name not in product_map.keys():
                        product_map[name] = [scan_count, accepted_count]
                    else:
                        product_map[name][0] += scan_count
                        product_map[name][1] += accepted_count

        ret = []
        for key in product_map:
            scan = product_map[key][0]
            accepted = product_map[key][1]
            ret.append(create_product_item(key, accepted / scan * 100 if scan != 0 else 100))

        return ret
