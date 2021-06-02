from typing import Optional

from pylti1p3.oidc_login import OIDCLogin
from pylti1p3.tool_config import ToolConfDict
from starlette.responses import HTMLResponse

from .cookie import StarletteCookieService
from .redirect import StarletteRedirect
from .request import StarletteRequest
from .session import StarletteSessionService


class StarletteOIDCLogin(OIDCLogin):

    def __init__(self,
                 request : StarletteRequest,
                 tool_config: ToolConfDict,
                 session_service: Optional[StarletteSessionService] = None,
                 cookie_service : Optional[StarletteCookieService] = None,
                 launch_data_storage=None):
        cookie_service = cookie_service if cookie_service else StarletteCookieService(request)
        session_service = session_service if session_service else StarletteSessionService(request)
        super().__init__(request, tool_config, session_service, cookie_service, launch_data_storage)

    def get_redirect(self, url):
        return StarletteRedirect(url,self._cookie_service)

    def get_response(self, html):
        return HTMLResponse(html)


