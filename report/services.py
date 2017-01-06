import sys
from wemark.commons import constants, utils


class Cacheable(object):
    def __init__(self, prefix):
        super(Cacheable, self).__init__()
        self.prefix = prefix

    def has_cache(self, key):
        full_key = self.prefix + key
        return False

    def cache(self, key, value, expires_in):
        full_key = self.prefix + key

    def get_cache(self, key):
        full_key = self.prefix + key


class AwardService(Cacheable):
    CACHE_AWARD_PREFIX = 'cache_award_key:'
    CACHE_AWARD_COUNT_KEY = "award_count"
    CACHE_AWARD_AMOUNT_KEY = "award_amount"

    def __init__(self):
        super(AwardService, self).__init__(AwardService.CACHE_AWARD_PREFIX)
        self.error_message = None

    def get_award_count(self):
        pass

    def get_award_amount(self):
        pass

    def fetch_by_batch_id(self, batch_id, accept_location, start_accept_time,
                          end_accept_time=utils.current_timestamp_in_millis(),
                          user_type=constants.WECHAT_USER_TYPE):
        pass

    def fetch_all(self, batch_ids, accept_location, start_accept_time,
                  end_accept_time=utils.current_timestamp_in_millis(),
                  user_type=constants.WECHAT_USER_TYPE):
        pass

    def get_error_message(self):
        return self.error_message


class BatchService(Cacheable):
    CACHE_BATCH_PREFIX = 'cache_batch_key:'
    CACHE_BATCH_IDS_KEY = 'batch_ids'

    def __init__(self):
        super(BatchService, self).__init__(BatchService.CACHE_BATCH_PREFIX)
        self.error_message = None

    def get_batch_ids(self):
        pass

    def fetch(self, start_created_time, end_created_time=utils.current_timestamp_in_millis(), incode_factory=None,
              outcode_factory=None, casecode_factory=None, case_count=None, min_case_count=0,
              max_case_count=sys.maxint, unit_count=None, min_unit_count=0, max_unit_count=sys.maxint,
              status=constants.BATCH_DONE_STATUS):
        pass

    def get_error_message(self):
        return self.error_message


class ScanCodeService(Cacheable):
    CACHE_SCAN_CODE_PREFIX = 'cache_scan_code_key:'
    CACHE_SCAN_CODE_COUNT_KEY = 'scan_code_count'

    def __init__(self):
        super(ScanCodeService, self).__init__(ScanCodeService.CACHE_SCAN_CODE_PREFIX)
        self.error_message = None

    def get_scan_count(self):
        pass

    def fetch_by_batch_id(self, batch_id, location, start_time, end_time=utils.current_timestamp_in_millis(),
                          func=constants.LOTTERY_SCAN, user_type=constants.WECHAT_USER_TYPE, min_times=0,
                          max_times=sys.maxint):
        pass

    def fetch_all(self, batch_ids, location, start_time, end_time=utils.current_timestamp_in_millis(),
                  func=constants.LOTTERY_SCAN, user_type=constants.WECHAT_USER_TYPE, min_times=0,
                  max_times=sys.maxint):
        pass

    def get_error_message(self):
        return self.error_message
