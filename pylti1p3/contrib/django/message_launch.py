from pylti1p3.message_launch import MessageLaunch
from pylti1p3.request import Request
from .cookie import DjangoCookieService
from .request import DjangoRequest
from .session import DjangoSessionService


class DjangoMessageLaunch(MessageLaunch):

    def __init__(self, request, tool_config, session_service=None, cookie_service=None, launch_data_storage=None):
        django_request = request if isinstance(request, Request) else DjangoRequest(request, post_only=True)
        cookie_service = cookie_service if cookie_service else DjangoCookieService(django_request)
        session_service = session_service if session_service else DjangoSessionService(request)
        super(DjangoMessageLaunch, self).__init__(django_request, tool_config, session_service, cookie_service,
                                                  launch_data_storage)

    def _get_request_param(self, key):
        return self._request.get_param(key)
