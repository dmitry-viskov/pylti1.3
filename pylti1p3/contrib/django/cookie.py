from pylti1p3.cookie import CookieService


class DjangoCookieService(CookieService):
    _request = None
    _cookie_data_to_set = None

    def __init__(self, request):
        self._request = request
        self._cookie_data_to_set = {}

    def _get_key(self, key):
        return self._cookie_prefix + '-' + key

    def get_cookie(self, name):
        return self._request.get_cookie(self._get_key(name))

    def set_cookie(self, name, value, exp=3600):
        self._cookie_data_to_set = {
            'key': self._get_key(name),
            'value': value,
            'exp': exp
        }

    def update_response(self, response):
        if self._cookie_data_to_set:
            response.set_cookie(
                self._cookie_data_to_set['key'],
                self._cookie_data_to_set['value'],
                max_age=self._cookie_data_to_set['exp'],
                path='/')
