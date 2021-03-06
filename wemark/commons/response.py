from django.http import JsonResponse


class ResponseEntity(object):
    RET_ERROR_CODE = 'error_code'
    RET_ERROR_DESCRIPTION = 'error_description'
    RET_DATA = 'data'

    @staticmethod
    def ok(data_map=None):
        ret = {
            ResponseEntity.RET_ERROR_CODE: ResponseResult.RET_OK[0],
            ResponseEntity.RET_ERROR_DESCRIPTION: ResponseResult.RET_OK[1]
        }
        if data_map is not None:
            ret[ResponseEntity.RET_DATA] = data_map

        return JsonResponse(ret)

    @staticmethod
    def bad_request(error_description=None):
        ret = {
            ResponseEntity.RET_ERROR_CODE: ResponseResult.RET_BAD_REQUEST[0],
            ResponseEntity.RET_ERROR_DESCRIPTION: error_description if error_description is not None else
            ResponseResult.RET_BAD_REQUEST[1]
        }

        return JsonResponse(ret)

    @staticmethod
    def server_error():
        ret = {
            ResponseEntity.RET_ERROR_CODE: ResponseResult.SERVER_ERROR[0],
            ResponseEntity.RET_ERROR_DESCRIPTION: ResponseResult.SERVER_ERROR[1]
        }

        return JsonResponse(ret)


class ResponseResult(object):
    RET_OK = (0, 'ok')
    RET_BAD_REQUEST = (-1, 'bad request')
    SERVER_ERROR = (-2, 'server error')

    @staticmethod
    def is_ok(err_code):
        return err_code == ResponseResult.RET_OK[0]


class Schema(object):
    HTTP = 'http'
    HTTPS = 'https'
