import time
import constants


def current_timestamp_in_millis():
    return long(time.time() * constants.TIME_MILLIS_UNIT)
