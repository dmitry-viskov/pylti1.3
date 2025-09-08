from fastapi.responses import HTMLResponse

from pylti1p3.oidc_login import OIDCLogin

from .cookie import FastAPICookieService
from .redirect import FastAPIRedirect
from .session import FastAPISessionService


class FastAPIOIDCLogin(OIDCLogin):
    def __init__(
        self,
        request,
        tool_config,
        session_service=None,
        cookie_service=None,
        launch_data_storage=None,
    ):
        cookie_service = (
            cookie_service if cookie_service else FastAPICookieService(request)
        )
        session_service = (
            session_service if session_service else FastAPISessionService(request)
        )
        super().__init__(
            request,
            tool_config,
            session_service,
            cookie_service,
            launch_data_storage,
        )

    def get_redirect(self, url):
        return FastAPIRedirect(url, self._cookie_service)

    def get_response(self, html):
        return HTMLResponse(content=html)
