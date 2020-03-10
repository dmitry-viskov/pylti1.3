from flask import session

from pylti1p3.request import Request


class FlaskRequest(Request):
    _request = None
    _cookies = []

    def __init__(self, _request: dict, _cookies: dict, _session: session):
        self.set_request(_request)
        self.session = _session
        self._cookies = _cookies

    def get_param(self, key: str) -> str:
        return self._request.get(key)

    def set_request(self, request: dict):
        self._request = request

    def get_cookie(self, key: str) -> str:
        return self._cookies.get(key)
