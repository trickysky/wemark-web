from django.http import HttpRequest
from django.http import HttpResponse

class AuthenticationMiddleware(object):
    def process_request(self, request):
        """
        global interception
        :type request: HttpRequest
        """
        pass

    def process_response(self, request, response):
        """
        global interception
        :param request: HttpRequest
        :type response: HttpResponse
        """
        pass

    def process_view(self, request):
        pass

    def process_exception(self, request, response):
        pass

    def process_template_response(self, request, response):
        pass
