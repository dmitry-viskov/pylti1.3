import asyncio

from starlette.requests import Request as _StarletteRequest
from pylti1p3.request import Request


class StarletteRequest(Request):
    def __init__(self, request: _StarletteRequest):
        super().__init__()
        self._request = request

    @property
    def session(self):
        return self._request.session

    def get_param(self, key) -> str:
        if self._request.method == 'GET':
            return self._request.query_params.get(key, None)
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            form_data = loop.run_until_complete(self._request.form())
            return form_data.get(key, None)

    def get_cookie(self, key):
        return self._request.cookies.get(key)

    def is_secure(self):
        return self._request.url.is_secure
