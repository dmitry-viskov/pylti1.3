from pylti1p3.request import Request


class FlaskRequest(Request):
    _request = None
    _cookies = []

    def __init__(self, request_kwargs, cookies, session, is_secure):
        self.set_request(request_kwargs)
        self.session = session
        self._cookies = cookies
        self._is_secure = is_secure

    def get_param(self, key):
        return self._request.get(key)

    def set_request(self, request):
        self._request = request

    def get_cookie(self, key):
        return self._cookies.get(key)

    def is_secure(self):
        return self._is_secure
