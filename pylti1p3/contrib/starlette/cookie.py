from pylti1p3.cookie import CookieService
from .request import StarletteRequest
from starlette.responses import Response


class StarletteCookieService(CookieService):

    def __init__(self, request: StarletteRequest) -> None:
        self._request = request
        self._cookie_data_to_set = {}

    def _get_key(self, key):
        return self._cookie_prefix + '-' + key

    def get_cookie(self, name):
        return self._request.get_cookie(self._get_key(name))

    def set_cookie(self, name, value, exp=3600):
        self._cookie_data_to_set[self._get_key(name)] = {
            'value': value,
            'exp': exp
        }

    def update_response(self, response: Response):
        for key, cookie_data in self._cookie_data_to_set.items():
            response.set_cookie(key=key,
                                value=cookie_data['value'],
                                expires=cookie_data['exp'],
                                secure=self._request.is_secure(),
                                path='/',
                                samesite='None')
