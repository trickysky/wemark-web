import requests
import logging
from django.contrib.sessions.backends.base import SessionBase

from services import AuthorizationService
from utils import OAuth2Utils, OAuth2RequestBuilder, ResponseType, GrantType, Scope
from wemark.commons import constants
from wemark.commons.response import ResponseEntity, ResponseResult
from wemark.commons.utils import is_not_null_or_empty


class Subject(object):
    SESSION_EXPIRES_IN = 30 * constants.TIME_HOUR_UNIT * constants.TIME_MINUTE_UNIT * constants.TIME_SECOND_UNIT

    SESSION_OPEN_ID = "session_open_id"
    SESSION_USER_INFO = "session_user_info"
    SESSION_ACCESS_TOKEN = "session_access_token"
    SESSION_REFRESH_TOKEN = "session_refresh_token"
    SESSION_ROLE = "session_role"
    SESSION_PERMISSIONS = "session_permissions"

    def __init__(self, session):
        """
        :type session: SessionBase
        """
        super(Subject, self).__init__()
        self.session = session

    def is_authenticated(self):
        if self.__validate_access_token() or self.__refresh_token():
            return True
        self.__clear()
        return False

    @staticmethod
    def redirect_to_authenticate(state=None):
        builder = Subject.__create_oauth2_builder(OAuth2Utils.SEGMENT_AUTHORIZE)

        builder.set_response_type(ResponseType.CODE).set_client_id(constants.CLIENT_ID) \
            .set_redirect_uri(constants.CLIENT_CALLBACK_URI).set_scope(Scope.WEB_LOGIN)
        if is_not_null_or_empty(state):
            builder.set_state(state)

        return builder.build() if builder.validate() else None

    def authenticate(self, auth_code):
        builder = Subject.__create_oauth2_builder(OAuth2Utils.SEGMENT_ACCESS_TOKEN)

        builder.set_client_id(constants.CLIENT_ID).set_client_secret(constants.CLIENT_SECRET).set_code(auth_code) \
            .set_grant_type(GrantType.AUTHORIZATION_CODE).set_redirect_uri(constants.CLIENT_CALLBACK_URI)

        if builder.validate():
            url = builder.build()
            r = requests.post(url=url, headers=self.__create_headers()).json()
            data = r.get(ResponseEntity.RET_DATA)
            if ResponseResult.is_ok(r.get(ResponseEntity.RET_ERROR_CODE)) and data:
                self.__update_session_by_data(data=data)
                self.get_user_info(force_update=True)
                self.__expire_all()
                return True
            else:
                logging.error(r)

        return False

    def logout(self):
        refresh_token = self.get_session_by_key(Subject.SESSION_REFRESH_TOKEN)
        self.__clear()

        if refresh_token:
            builder = Subject.__create_oauth2_builder(OAuth2Utils.SEGMENT_LOG_OFF)
            builder.set_refresh_token(refresh_token).set_client_id(constants.CLIENT_ID)
            if builder.validate():
                url = builder.build()
                r = requests.post(url=url, headers=self.__create_headers()).json()
                return ResponseResult.is_ok(r.get(ResponseEntity.RET_ERROR_CODE))

        return False

    def __validate_access_token(self):
        if self.exists(Subject.SESSION_ACCESS_TOKEN) and self.exists(Subject.SESSION_OPEN_ID):
            builder = OAuth2RequestBuilder()
            builder.set_access_token(Subject.SESSION_ACCESS_TOKEN).set_client_id(constants.CLIENT_ID) \
                .set_open_id(self.get_session_by_key(Subject.SESSION_OPEN_ID))
            if builder.validate():
                url = builder.build()
                r = requests.get(url=url, headers=self.__create_headers()).json()
                return ResponseResult.is_ok(r.get(ResponseEntity.RET_ERROR_CODE))
        return False

    def __refresh_token(self):
        if not self.exists(Subject.SESSION_REFRESH_TOKEN):
            return False

        refresh_token = self.get_session_by_key(Subject.SESSION_REFRESH_TOKEN)
        builder = self.__create_oauth2_builder(OAuth2Utils.SEGMENT_REFRESH_TOKEN)
        builder.set_client_id(constants.CLIENT_ID).set_client_secret(constants.CLIENT_SECRET).set_grant_type(
            GrantType.REFRESH_TOKEN).set_refresh_token(refresh_token)
        if builder.validate():
            url = builder.build()
            r = requests.post(url=url, headers=self.__create_headers()).json()
            data = r.get(ResponseEntity.RET_DATA)
            if ResponseResult.is_ok(r.get(ResponseEntity.RET_ERROR_CODE)) and data:
                self.__update_session_by_data(data=data)
                self.__expire_all()
                return True
            else:
                logging.error(r)

        return False

    def get_user_info(self, force_update=False):
        info_cached = self.get_session_by_key(Subject.SESSION_USER_INFO)
        if not force_update and info_cached is not None:
            return info_cached

        builder = self.__create_oauth2_builder(OAuth2Utils.SEGMENT_GET_USER_INFO)
        open_id = self.get_session_by_key(Subject.SESSION_OPEN_ID)
        access_token = self.get_session_by_key(Subject.SESSION_ACCESS_TOKEN)
        builder.set_open_id(open_id).set_access_token(access_token).set_client_id(constants.CLIENT_ID)
        if builder.validate():
            url = builder.build()
            r = requests.get(url=url, headers=self.__create_headers()).json()
            data = r.get(ResponseEntity.RET_DATA)
            if ResponseResult.is_ok(r.get(ResponseEntity.RET_ERROR_CODE)) and data:
                self.add_or_update_session_by_key(Subject.SESSION_USER_INFO, data)
                return data

        return None

    def get_session(self):
        return self.session

    def has_role(self, role_name):
        return self.exists(Subject.SESSION_ROLE) and self.get_session_by_key(Subject.SESSION_ROLE) == role_name

    def has_permission(self, permission_name):
        if not self.exists(Subject.SESSION_ROLE):
            return False

        role_name = self.get_session_by_key(Subject.SESSION_ROLE)
        permissions = AuthorizationService.get_permissions_by_role_name(role_name=role_name)
        resource, operation = AuthorizationService.parse_permission(permission_name)
        if resource and operation:
            operations = permissions.get(resource)
            return operation in operations

        return False

    def get_session_by_key(self, key):
        return self.session.get(key, default=None)

    def add_or_update_session_by_key(self, key, value):
        self.session[key] = value

    def add_or_update_session_by_dict(self, dict_obj):
        for key in dict_obj:
            self.add_or_update_session_by_key(key, dict_obj[key])

    def delete_session_by_key(self, key):
        if self.session.get(key):
            del self.session[key]

    def exists(self, key):
        return self.get_session_by_key(key) is not None

    def __clear(self):
        for key in [Subject.SESSION_OPEN_ID, Subject.SESSION_USER_INFO, Subject.SESSION_ACCESS_TOKEN,
                    Subject.SESSION_REFRESH_TOKEN, Subject.SESSION_ROLE, Subject.SESSION_PERMISSIONS]:
            self.delete_session_by_key(key)

    def __expire_all(self):
        self.session.set_expiry(Subject.SESSION_EXPIRES_IN)

    def __update_session_by_data(self, data):
        role_name = data.get(OAuth2Utils.ROLE)
        session_kv = {
            Subject.SESSION_ACCESS_TOKEN: data.get(OAuth2Utils.ACCESS_TOKEN),
            Subject.SESSION_REFRESH_TOKEN: data.get(OAuth2Utils.REFRESH_TOKEN),
            Subject.SESSION_ROLE: role_name,
            Subject.SESSION_OPEN_ID: data.get(OAuth2Utils.OPEN_ID),
        }
        self.add_or_update_session_by_dict(session_kv)

    @staticmethod
    def __create_oauth2_builder(segment):
        return OAuth2RequestBuilder().set_schema(constants.OAUTH2_SCHEMA).set_host(constants.OAUTH2_HOST) \
            .set_port(constants.OAUTH2_PORT).set_segment(segment)

    @staticmethod
    def __create_headers():
        return {
            'content-type': 'application/x-www-form-urlencoded',
        }

    @staticmethod
    def get_instance(session):
        return Subject(session)
