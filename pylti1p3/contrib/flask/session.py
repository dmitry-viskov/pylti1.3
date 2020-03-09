from pylti1p3.session import SessionService

from .request import FlaskRequest


class FlaskSessionService(SessionService):
    _request = None

    def __init__(self, request: FlaskRequest):
        self._request = request

    def _get_key(self, key: str, nonce=None):
        return self._session_prefix + '-' + key + \
               (('-' + nonce) if nonce else '')

    def get_launch_data(self, key: str) -> str:
        return self._request.session.get(self._get_key(key), None)

    def save_launch_data(self, key: str, jwt_body: str):
        self._request.session[self._get_key(key)] = jwt_body

    def save_nonce(self, nonce: str):
        self._request.session[self._get_key('nonce', nonce)] = True

    def check_nonce(self, nonce: str) -> bool:
        return self._get_key('nonce', nonce) in self._request.session

    def save_state_params(self, state: str, params: dict):
        self._request.session[self._get_key(state)] = params

    def get_state_params(self, state: str) -> dict:
        return self._request.session[self._get_key(state)]
