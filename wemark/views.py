from django.http import HttpRequest, HttpResponseRedirect


def index(request):
    """
    :type request: HttpRequest
    """
    redirect_uri = '/report'
    return HttpResponseRedirect(redirect_to=redirect_uri)
