from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest

from oauth2.commons.security import Subject
from commons import constants


class AuthenticationMiddleware(MiddlewareMixin):
    EXCEPTIONS = ['/oauth2/callback', '/error']

    @staticmethod
    def process_request(request):
        """
        :type request: HttpRequest
        """
        if AuthenticationMiddleware.get_client_ip(request) in constants.LOCALHOST:
            return None
        subject = Subject.get_instance(request.session)
        if request.path not in AuthenticationMiddleware.EXCEPTIONS and not subject.is_authenticated():
            redirect_uri = subject.redirect_to_authenticate()
            if redirect_uri:
                return HttpResponseRedirect(redirect_uri)
            else:
                return HttpResponseRedirect('/error')
        return None

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
