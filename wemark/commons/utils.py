import time
import constants


def current_timestamp_in_millis():
    return long(time.time() * constants.TIME_MILLIS_UNIT)


def is_not_null_or_empty(string):
    return string is not None and string != ''


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
