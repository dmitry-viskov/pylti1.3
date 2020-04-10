from pylti1p3.message_launch import MessageLaunch
from .cookie import FlaskCookieService
from .session import FlaskSessionService


class FlaskMessageLaunch(MessageLaunch):

    def __init__(self, request, tool_config, session_service=None, cookie_service=None, launch_data_storage=None):
        cookie_service = cookie_service if cookie_service else FlaskCookieService(request)
        session_service = session_service if session_service else FlaskSessionService(request)
        super(FlaskMessageLaunch, self).__init__(request, tool_config, session_service, cookie_service,
                                                 launch_data_storage)

    def _get_request_param(self, key):
        return self._request.get_param(key)
