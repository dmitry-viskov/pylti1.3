from pylti1p3.oidc_login import OIDCLogin
from .cookie import DjangoCookieService
from .redirect import DjangoRedirect
from .request import DjangoRequest
from .session import DjangoSessionService


class DjangoOIDCLogin(OIDCLogin):

    def __init__(self, request, tool_config):
        django_request = DjangoRequest(request)
        cookie_service = DjangoCookieService(django_request)
        session_service = DjangoSessionService(request)
        super(DjangoOIDCLogin, self).__init__(django_request, tool_config, session_service, cookie_service)

    def get_redirect(self, url):
        return DjangoRedirect(url, self._cookie_service)
