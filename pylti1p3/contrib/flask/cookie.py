from pylti1p3.cookie import CookieService
from werkzeug.wrappers import Response

from .request import FlaskRequest


class FlaskCookieService(CookieService):
    _request = None
    _cookie_data_to_set = None

    def __init__(self, request: FlaskRequest):
        self._request = request
        self._cookie_data_to_set = {}

    def _get_key(self, key: str) -> str:
        return self._cookie_prefix + '-' + key

    def get_cookie(self, name: str) -> str:
        return self._request.get_cookie(self._get_key(name))

    def set_cookie(self, name: str, value: str, exp=3600):
        self._cookie_data_to_set = {
            'key': self._get_key(name),
            'value': value,
            'exp': exp
        }

    def update_response(self, response: Response):
        if self._cookie_data_to_set:
            response.set_cookie(
                self._cookie_data_to_set['key'],
                self._cookie_data_to_set['value'],
                max_age=self._cookie_data_to_set['exp'],
                path='/')
