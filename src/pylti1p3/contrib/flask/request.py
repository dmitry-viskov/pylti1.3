from flask import request  # type: ignore
from flask import session as flask_session
from pylti1p3.request import Request


class FlaskRequest(Request):
    _cookies = None
    _request_data = None
    _request_is_secure = None
    _session = None

    def __init__(
        self, cookies=None, session=None, request_data=None, request_is_secure=None
    ):
        super().__init__()
        self._cookies = request.cookies if cookies is None else cookies
        self._session = flask_session if session is None else session
        self._request_is_secure = (
            request.is_secure if request_is_secure is None else request_is_secure
        )

        if request_data:
            self._request_data = request_data

    @property
    def session(self):
        return self._session

    def get_param(self, key):
        if self._request_data:
            return self._request_data.get(key)
        if request.method == "GET":
            return request.args.get(key, None)
        return request.form.get(key, None)

    def get_cookie(self, key):
        return self._cookies.get(key)

    def is_secure(self):
        return self._request_is_secure
