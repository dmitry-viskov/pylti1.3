import typing as t
import uuid
from abc import ABCMeta, abstractmethod

from .actions import Action
from .exception import OIDCException

if t.TYPE_CHECKING:
    from .cookie import CookieService
    from .request import Request
    from .session import SessionService
    from .redirect import Redirect
    from .tool_config import ToolConfAbstract
    from .registration import Registration

    def urlencode(url):
        # type: (t.Dict[str, str]) -> str
        return str(url)
else:
    try:
        from urllib import urlencode
    except ImportError:
        from urllib.parse import urlencode

RED = t.TypeVar('RED')
REQ = t.TypeVar('REQ', bound='Request')
TCONF = t.TypeVar('TCONF', bound='ToolConfAbstract')
SES = t.TypeVar('SES', bound='SessionService')
COOK = t.TypeVar('COOK', bound='CookieService')


class OIDCLogin(t.Generic[REQ, TCONF, SES, COOK, RED]):
    __metaclass__ = ABCMeta
    _request = None  # type: REQ
    _tool_config = None  # type: TCONF
    _session_service = None  # type: SES
    _cookie_service = None  # type: COOK
    _state_params = {}  # type: t.Dict[str, object]

    def __init__(self, request, tool_config, session_service, cookie_service):
        # type: (REQ, TCONF, SES, COOK) -> None
        self._request = request
        self._tool_config = tool_config
        self._session_service = session_service
        self._cookie_service = cookie_service

    @abstractmethod
    def get_redirect(self, url):
        # type: (str) -> Redirect[RED]
        raise NotImplementedError

    def _get_request_param(self, key):
        # type: (str) -> t.Any
        return self._request.get_param(key)

    def _get_uuid(self):
        # type: () -> str
        return str(uuid.uuid4())

    def _prepare_redirect(self, launch_url):
        # type: (str) -> Redirect[RED]
        if not launch_url:
            raise OIDCException("No launch URL configured")

        # validate request
        registration = self.validate_oidc_login()

        # build OIDC Auth Response

        # generate state
        # set cookie (short lived)
        state = 'state-' + self._get_uuid()
        self._cookie_service.set_cookie(state, state)

        # generate nonce
        nonce = self._get_uuid()
        self._session_service.save_nonce(nonce)
        if self._state_params:
            self._session_service.save_state_params(state, self._state_params)

        # build Response
        client_id = registration.get_client_id()  # Registered client id
        assert client_id is not None, 'Client id should not be None'
        auth_params = {
            'scope': 'openid',  # OIDC Scope
            'response_type': 'id_token',  # OIDC response is always an id token
            'response_mode': 'form_post',  # OIDC response is always a form post
            'prompt': 'none',  # Don't prompt user on redirect
            'client_id': client_id,
            'redirect_uri': launch_url,  # URL to return to after login
            'state': state,  # State to identify browser session
            'nonce': nonce,  # Prevent replay attacks
            'login_hint':  self._get_request_param('login_hint')  # Login hint to identify platform session
        }

        # pass back LTI message hint if we have it
        lti_message_hint = self._get_request_param('lti_message_hint')
        if lti_message_hint:
            # LTI message hint to identify LTI context within the platform
            auth_params['lti_message_hint'] = lti_message_hint

        auth_login_return_url = registration.get_auth_login_url()
        assert auth_login_return_url is not None, 'Auth login url of registration is None'
        auth_login_return_url += "?" + urlencode(auth_params)

        # return auth redirect
        return self.get_redirect(auth_login_return_url)

    def redirect(self, launch_url, js_redirect=False):
        # type: (str, bool) -> RED
        """
        Calculate the redirect location to return to based on an OIDC third party initiated login request.

        :param launch_url: URL to redirect back to after the OIDC login.
        This URL must match exactly a URL white listed in the platform.
        :param js_redirect: Redirect through JS
        :return: Returns a redirect object containing the fully formed OIDC login URL.
        """
        redirect_obj = self._prepare_redirect(launch_url)
        if js_redirect:
            return redirect_obj.do_js_redirect()
        return redirect_obj.do_redirect()

    def get_redirect_object(self, launch_url):
        # type: (str) -> Redirect[RED]
        return self._prepare_redirect(launch_url)

    def validate_oidc_login(self):
        # type: () -> Registration
        # validate Issuer
        iss = self._get_request_param('iss')
        if not iss:
            raise OIDCException('Could not find issuer')

        # validate login hint
        login_hint = self._get_request_param('login_hint')
        if not login_hint:
            raise OIDCException('Could not find login hint')

        # fetch registration details
        registration = self._tool_config.find_registration(iss, action=Action.OIDC_LOGIN, request=self._request)

        # check we got something
        if not registration:
            raise OIDCException("Could not find registration details")

        return registration

    def pass_params_to_launch(self, params):
        # type: (t.Dict[str, object]) -> None
        """
        Ability to pass custom params from oidc login to launch.
        """
        self._state_params = params
