import requests
from django.contrib.sessions.backends.base import SessionBase
import constants


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
        if self.session[Subject.SESSION_ACCESS_TOKEN] and self.__validate_access_token() \
                or self.session[Subject.SESSION_REFRESH_TOKEN] and self.refresh_token():
            return True
        self.__clear()
        return False

    def authenticate(self, auth_code):
        pass

    def logout(self):
        pass

    def get_session(self):
        return self.session

    def has_role(self, role_name):
        return role_name == self.session[Subject.SESSION_ROLE]

    def has_permission(self, permission_name):
        return permission_name in self.session[Subject.SESSION_PERMISSIONS]

    def refresh_token(self):
        pass

    def expire_all(self):
        pass

    def get_user_info(self):
        pass

    def get_open_id(self):
        pass

    def __validate_access_token(self):
        pass

    def __clear(self):
        for key in [Subject.SESSION_OPEN_ID, Subject.SESSION_USER_INFO, Subject.SESSION_ACCESS_TOKEN,
                    Subject.SESSION_REFRESH_TOKEN, Subject.SESSION_ROLE, Subject.SESSION_PERMISSIONS]:
            self.__delete_session_by_key(key)

    def __delete_session_by_key(self, key):
        if self.session[key]:
            del self.session[key]

    @staticmethod
    def get_instance(request):
        return Subject(request)
