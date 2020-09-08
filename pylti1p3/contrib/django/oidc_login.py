from django.http import HttpResponse  # type: ignore
from pylti1p3.oidc_login import OIDCLogin
from pylti1p3.request import Request

from .cookie import DjangoCookieService
from .redirect import DjangoRedirect
from .request import DjangoRequest
from .session import DjangoSessionService


class DjangoOIDCLogin(OIDCLogin):

    def __init__(self, request, tool_config, session_service=None, cookie_service=None, launch_data_storage=None):
        django_request = request if isinstance(request, Request) else DjangoRequest(request)
        cookie_service = cookie_service if cookie_service else DjangoCookieService(django_request)
        session_service = session_service if session_service else DjangoSessionService(request)
        super(DjangoOIDCLogin, self).__init__(django_request, tool_config, session_service, cookie_service,
                                              launch_data_storage)

    def get_redirect(self, url):
        return DjangoRedirect(url, self._cookie_service)

    def get_response(self, html):
        return HttpResponse(html)
