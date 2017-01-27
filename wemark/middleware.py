from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest

from oauth2.commons.security import Subject


class AuthenticationMiddleware(MiddlewareMixin):
    EXCEPTIONS = ['/oauth2/callback', '/error']

    @staticmethod
    def process_request(request):
        """
        :type request: HttpRequest
        """
        subject = Subject.get_instance(request.session)
        if request.path not in AuthenticationMiddleware.EXCEPTIONS and not subject.is_authenticated():
            redirect_uri = subject.redirect_to_authenticate(request=request, state=request.get_raw_uri())
            if redirect_uri:
                return HttpResponseRedirect(redirect_uri)
            else:
                return HttpResponseRedirect('/error')
        return None


class MultipleProxyMiddleware(MiddlewareMixin):
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def process_request(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()
