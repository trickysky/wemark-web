from wemark.commons.response import Schema

TIME_HOUR_UNIT = 24
TIME_MINUTE_UNIT = 60
TIME_SECOND_UNIT = 60
TIME_MILLIS_UNIT = 1000

CLIENT_ID = 'dd055109e309a4c8'
CLIENT_SECRET = '83eb90109062909b03ceb2efa13016f9'
CLIENT_CALLBACK_URI = '/oauth2/callback'

OAUTH2_SCHEMA = Schema.HTTP
OAUTH2_HOST = 'auth.spoonsea.com'
OAUTH2_PORT = 80

LOCALHOST = ['localhost', '127.0.0.1']

UNIT_CHINA_FEN = 100


class ScanCode(object):
    Lottery = 1
    Traceability = 2


class UserType(object):
    Wechat = 1
    Dealer = 99
    Factory = 100


class AssignType(object):
    Outer = 0
    Inner = 1
    Case = 2


class BatchStatus(object):
    Discard = -1
    Done = 0
    Proceeding = 1
    Ready = 2
    Downloading = 3
    Downloaded = 4


class ProductStatus(object):
    Normal = 0
    Removed = 1
    Abnormal = -1