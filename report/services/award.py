from report.commons import utils
from report.commons import constants
from report.services.cacheable import Cacheable


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
