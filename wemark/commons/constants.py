from wemark.commons.response import Schema

TIME_HOUR_UNIT = 24
TIME_MINUTE_UNIT = 60
TIME_SECOND_UNIT = 60
TIME_MILLIS_UNIT = 1000

LOTTERY_SCAN = 1
TRACEABILITY_SCAN = 2

WECHAT_USER_TYPE = 1

BATCH_DISCARD_STATUS = -1
BATCH_DONE_STATUS = 0
BATCH_PROCEEDING_STATUS = 1
BATCH_READY_STATUS = 2
BATCH_DOWNLOADING_STATUS = 3
BATCH_DOWNLOADED_STATUS = 4

CLIENT_ID = 'dd055109e309a4c8'
CLIENT_SECRET = '83eb90109062909b03ceb2efa13016f9'
CLIENT_CALLBACK_URI = 'http://manage.spoonsea.com/oauth2/callback'
# CLIENT_CALLBACK_URI = 'http://localhost:8000/oauth2/callback'

OAUTH2_SCHEMA = Schema.HTTP
OAUTH2_HOST = 'auth.spoonsea.com'
OAUTH2_PORT = 80

LOCALHOST = ['localhost', '127.0.0.1']