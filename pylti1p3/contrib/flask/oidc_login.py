from flask import make_response  # type: ignore
from pylti1p3.oidc_login import OIDCLogin
from .cookie import FlaskCookieService
from .session import FlaskSessionService
from .redirect import FlaskRedirect


class FlaskOIDCLogin(OIDCLogin):
    def __init__(
        self,
        request,
        tool_config,
        session_service=None,
        cookie_service=None,
        launch_data_storage=None,
    ):
        cookie_service = (
            cookie_service if cookie_service else FlaskCookieService(request)
        )
        session_service = (
            session_service if session_service else FlaskSessionService(request)
        )
        super().__init__(
            request, tool_config, session_service, cookie_service, launch_data_storage
        )

    def get_redirect(self, url):
        return FlaskRedirect(url, self._cookie_service)

    def get_response(self, html):
        return make_response(html)
