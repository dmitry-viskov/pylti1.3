from pylti1p3.message_launch import MessageLaunch
from .cookie import FlaskCookieService
from .session import FlaskSessionService
from .service_connector import FlaskServiceConnector


class FlaskMessageLaunch(MessageLaunch):
    def __init__(
        self,
        request,
        tool_config,
        *,
        session_service=None,
        cookie_service=None,
        launch_data_storage=None,
        requests_session=None,
        service_connector_cls: type[FlaskServiceConnector] = FlaskServiceConnector,
    ):
        cookie_service = (
            cookie_service if cookie_service else FlaskCookieService(request)
        )
        session_service = (
            session_service if session_service else FlaskSessionService(request)
        )
        super().__init__(
            request=request,
            tool_config=tool_config,
            session_service=session_service,
            cookie_service=cookie_service,
            launch_data_storage=launch_data_storage,
            requests_session=requests_session,
            service_connector_cls=service_connector_cls,
        )

    def _get_request_param(self, key):
        return self._request.get_param(key)
