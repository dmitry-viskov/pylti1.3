import werkzeug

from pylti1p3.cookie import CookieService


class FlaskCookieService(CookieService):
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
            cookie_kwargs = dict(
                key=self._cookie_data_to_set['key'],
                value=self._cookie_data_to_set['value'],
                max_age=self._cookie_data_to_set['exp'],
                secure=self._request.is_secure(),
                path='/',
                httponly=True,
            )

            werkzeug_version = int(werkzeug.__version__.split('.')[0])
            if self._request.is_secure() and werkzeug_version >= 1:
                cookie_kwargs['samesite'] = 'None'

            response.set_cookie(**cookie_kwargs)
