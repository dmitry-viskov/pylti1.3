from flask import request, session as flask_session

from pylti1p3.request import Request


class FlaskRequest(Request):
    session = None
    _cookies = None
    _request_data = None
    _request_is_secure = None

    def __init__(self, cookies=None, session=None, request_data=None, request_is_secure=None):
        self._cookies = request.cookies if cookies is None else cookies
        self.session = flask_session if session is None else session
        self._request_is_secure = request.is_secure if request_is_secure is None else request_is_secure

        if request_data:
            self._request_data = request_data

    def get_param(self, key):
        if self._request_data:
            return self._request_data.get(key)
        else:
            if request.method == 'GET':
                return request.args.get(key, None)
            else:
                return request.form.get(key, None)

    def get_cookie(self, key):
        return self._cookies.get(key)

    def is_secure(self):
        return self._request_is_secure
