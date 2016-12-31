import time
from urllib import unquote
from urllib import urlencode
from urllib import quote_plus
import urlparse

import constants


def current_timestamp_in_millis():
    return long(time.time() * constants.TIME_MILLIS_UNIT)


class OAuth2Utils(object):
    SEGMENT_AUTHORIZE = 'authorize'
    SEGMENT_ACCESS_TOKEN = 'access_token'
    SEGMENT_REFRESH_TOKEN = 'refresh_token'
    SEGMENT_VALIDATE = 'validate'
    SEGMENT_GET_USER_INFO = 'info'
    SEGMENT_LOG_OFF = 'logoff_authorization'

    RET_ERROR_CODE = 'error_code'
    RET_ERROR_DESCRIPTION = 'error_description'

    CLIENT_ID = 'client_id'
    CLIENT_SECRET = 'client_secret'
    RESPONSE_TYPE = 'response_type'
    STATE = 'state'
    REDIRECT_URI = 'redirect_uri'
    SCOPE = 'scope'
    AUTH_CODE = 'code'
    GRANT_TYPE = 'grant_type'
    REFRESH_TOKEN = 'refresh_token'
    ACCESS_TOKEN = 'access_token'
    EXPIRES_IN = 'expires_in'
    OPEN_ID = 'openid'


class ResponseType(object):
    CODE = 'code'


class GrantType(object):
    AUTHORIZATION_CODE = 'authorization_code'
    REFRESH_TOKEN = 'refresh_token'


class Scope(object):
    WEB_LOGIN = 'web_login'
    MOBILE_LOGIN = 'mobile_login'


class OAuth2RequestBuilder(object):
    SEPARATOR_OF_HOST_AND_PORT = ':'

    def __init__(self):
        super(OAuth2RequestBuilder, self).__init__()
        self.__schema = None
        self.__host = None
        self.__port = None
        self.__segment = None

        self.__params = {}

    def set_schema(self, schema):
        self.__schema = schema
        return self

    def set_host(self, host):
        self.__host = host
        return self

    def set_port(self, port):
        self.__port = port
        return self

    def set_segment(self, segment):
        self.__segment = segment
        return self

    def set_response_type(self, response_type):
        self.__params[OAuth2Utils.RESPONSE_TYPE] = response_type
        return self

    def set_client_id(self, client_id):
        self.__params[OAuth2Utils.CLIENT_ID] = client_id
        return self

    def set_client_secret(self, client_secret):
        self.__params[OAuth2Utils.CLIENT_SECRET] = client_secret
        return self

    def set_state(self, state):
        self.__params[OAuth2Utils.STATE] = state
        return self

    def set_redirect_uri(self, redirect_uri):
        self.__params[OAuth2Utils.REDIRECT_URI] = quote_plus(redirect_uri)
        return self

    def set_scope(self, scope):
        self.__params[OAuth2Utils.SCOPE] = scope
        return self

    def set_access_token(self, access_token):
        self.__params[OAuth2Utils.ACCESS_TOKEN] = access_token
        return self

    def set_refresh_token(self, refresh_token):
        self.__params[OAuth2Utils.REFRESH_TOKEN] = refresh_token
        return self

    def set_open_id(self, open_id):
        self.__params[OAuth2Utils.OPEN_ID] = open_id
        return self

    def validate(self):
        if not OAuth2Validator.validate_not_null_or_empty([self.__schema, self.__host]):
            return False

        if self.__segment == OAuth2Utils.SEGMENT_AUTHORIZE:
            return OAuth2Validator.validate_not_null_or_empty([
                self.__params[OAuth2Utils.RESPONSE_TYPE],
                self.__params[OAuth2Utils.CLIENT_ID],
                self.__params[OAuth2Utils.REDIRECT_URI],
                self.__params[OAuth2Utils.SCOPE]
            ]) and OAuth2Validator.validate_response_type(
                self.__params[OAuth2Utils.RESPONSE_TYPE], [ResponseType.CODE]
            ) and OAuth2Validator.validate_urlencoded_uri(
                self.__params[OAuth2Utils.REDIRECT_URI]
            ) and OAuth2Validator.validate_scope(
                self.__params[OAuth2Utils.SCOPE], [Scope.WEB_LOGIN])

        elif self.__segment == OAuth2Utils.SEGMENT_ACCESS_TOKEN:
            return OAuth2Validator.validate_not_null_or_empty([
                self.__params[OAuth2Utils.CLIENT_ID],
                self.__params[OAuth2Utils.CLIENT_SECRET],
                self.__params[OAuth2Utils.AUTH_CODE],
                self.__params[OAuth2Utils.GRANT_TYPE],
                self.__params[OAuth2Utils.REDIRECT_URI]
            ]) and OAuth2Validator.validate_grant_type(
                self.__params[OAuth2Utils.GRANT_TYPE], [GrantType.AUTHORIZATION_CODE]
            ) and OAuth2Validator.validate_urlencoded_uri(
                self.__params[OAuth2Utils.REDIRECT_URI])

        elif self.__segment == OAuth2Utils.SEGMENT_REFRESH_TOKEN:
            return OAuth2Validator.validate_not_null_or_empty([
                self.__params[OAuth2Utils.CLIENT_ID],
                self.__params[OAuth2Utils.CLIENT_SECRET],
                self.__params[OAuth2Utils.GRANT_TYPE],
                self.__params[OAuth2Utils.REFRESH_TOKEN]
            ]) and OAuth2Validator.validate_grant_type(
                self.__params[OAuth2Utils.GRANT_TYPE], [GrantType.REFRESH_TOKEN])

        elif self.__segment == OAuth2Utils.SEGMENT_VALIDATE:
            return OAuth2Validator.validate_not_null_or_empty([
                self.__params[OAuth2Utils.CLIENT_ID],
                self.__params[OAuth2Utils.OPEN_ID],
                self.__params[OAuth2Utils.ACCESS_TOKEN]
            ])

        elif self.__segment == OAuth2Utils.SEGMENT_GET_USER_INFO:
            return OAuth2Validator.validate_not_null_or_empty([
                self.__params[OAuth2Utils.OPEN_ID],
                self.__params[OAuth2Utils.ACCESS_TOKEN]
            ])

        elif self.__segment == OAuth2Utils.SEGMENT_LOG_OFF:
            return OAuth2Validator.validate_not_null_or_empty([
                self.__params[OAuth2Utils.REFRESH_TOKEN],
                self.__params[OAuth2Utils.CLIENT_ID]
            ])

        return False

    def build(self):
        queries = urlencode(self.__params)
        host_uri = self.__host
        if self.__port is not None:
            host_uri += OAuth2RequestBuilder.SEPARATOR_OF_HOST_AND_PORT + self.__port

        return urlparse.urlunsplit((self.__schema, host_uri, self.__segment, queries, ''))

    def get_uri(self):
        host_uri = self.__host
        if self.__port is not None:
            host_uri += OAuth2RequestBuilder.SEPARATOR_OF_HOST_AND_PORT + self.__port

        return urlparse.urlunsplit((self.__schema, host_uri, self.__segment, '', ''))

    def get_query_params(self):
        return self.__params


class OAuth2Validator(object):
    @staticmethod
    def validate_not_null_or_empty(fields):
        """
        :type fields: list
        """
        for field in fields:
            if field is None or field == '':
                return False
        return True

    @staticmethod
    def validate_urlencoded_uri(uri):
        decode_uri = unquote(uri)
        return decode_uri != uri

    @staticmethod
    def validate_response_type(response_type, answers):
        return response_type in answers

    @staticmethod
    def validate_scope(scope, answers):
        return scope in answers

    @staticmethod
    def validate_grant_type(grant_type, answers):
        return grant_type in answers
