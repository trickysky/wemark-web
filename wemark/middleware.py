from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest

from oauth2.commons.security import Subject


class AuthenticationMiddleware(MiddlewareMixin):
    EXCEPTIONS = ['/oauth2/callback', ]

    @staticmethod
    def process_request(request):
        """
        :type request: HttpRequest
        """
        subject = Subject.get_instance(request.session)
        if request.path not in AuthenticationMiddleware.EXCEPTIONS and not subject.is_authenticated():
            redirect_uri = subject.redirect_to_authenticate()
            if redirect_uri:
                return HttpResponseRedirect(redirect_uri)
            else:
                return HttpResponseRedirect('/error')
        return None
