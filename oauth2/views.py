from oauth2.commons.security import Subject
from oauth2.commons.utils import OAuth2Utils
from django.http import HttpResponseRedirect


def authorize(request):
    subject = Subject.get_instance(request.session)
    code = OAuth2Utils.parse_auth_code(request)
    state = OAuth2Utils.parse_state(request)

    if subject.authenticate(code):
        return HttpResponseRedirect(redirect_to='/report')
    else:
        HttpResponseRedirect(redirect_to=subject.redirect_to_authenticate(state=state))


def logout(request):
    subject = Subject.get_instance(request.session)
    subject.logout()
    return HttpResponseRedirect(redirect_to=subject.redirect_to_authenticate())
