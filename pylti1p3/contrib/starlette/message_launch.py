from typing import Optional

from pylti1p3.message_launch import MessageLaunch
from pylti1p3.tool_config import ToolConfDict

from .cookie import StarletteCookieService
from .request import StarletteRequest
from .session import StarletteSessionService


class StarletteMessageLaunch(MessageLaunch):

    def __init__(self,
                 request: StarletteRequest,
                 tool_config : ToolConfDict,
                 session_service: Optional[StarletteSessionService] = None,
                 cookie_service: Optional[StarletteCookieService] = None,
                 launch_data_storage=None):
        cookie_service = cookie_service if cookie_service else StarletteCookieService(request)
        session_service = session_service if session_service else StarletteSessionService(request)
        super().__init__(request, tool_config, session_service, cookie_service,
                         launch_data_storage)

    def _get_request_param(self, key):
        return self._request.get_param(key)
