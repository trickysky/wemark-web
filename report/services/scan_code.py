import sys
from report.commons import constants
from report.commons import utils
from report.services.cacheable import Cacheable


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
