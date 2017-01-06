import time
import constants


def current_timestamp_in_millis():
    return long(time.time() * constants.TIME_MILLIS_UNIT)


def is_not_null_or_empty(string):
    return string is not None and string != ''
