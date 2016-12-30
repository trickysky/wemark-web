import sys
from report.commons import constants
from report.commons import utils
from report.services.cacheable import Cacheable


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
              status=constants.BATCH_PROCESSING_STATUS):
        pass

    def get_error_message(self):
        return self.error_message
