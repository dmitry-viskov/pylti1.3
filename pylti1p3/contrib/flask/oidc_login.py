from pylti1p3.oidc_login import OIDCLogin
from .cookie import FlaskCookieService
from .session import FlaskSessionService
from .redirect import FlaskRedirect


class FlaskOIDCLogin(OIDCLogin):

    def __init__(self, request, tool_config, session_service=None, cookie_service=None):
        cookie_service = cookie_service if cookie_service else FlaskCookieService(request)
        session_service = session_service if session_service else FlaskSessionService(request)
        super(FlaskOIDCLogin, self).__init__(request, tool_config, session_service, cookie_service)

    def get_redirect(self, url):
        return FlaskRedirect(url, self._cookie_service)
