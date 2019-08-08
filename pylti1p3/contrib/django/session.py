from pylti1p3.session import SessionService


class DjangoSessionService(SessionService):
    _request = None

    def __init__(self, request):
        self._request = request

    def _get_key(self, key, nonce=None):
        return self._session_prefix + '-' + key + (('-' + nonce) if nonce else '')

    def get_launch_data(self, key):
        return self._request.session.get(self._get_key(key), None)

    def save_launch_data(self, key, jwt_body):
        self._request.session[self._get_key(key)] = jwt_body

    def save_nonce(self, nonce):
        self._request.session[self._get_key('nonce', nonce)] = True

    def check_nonce(self, nonce):
        nonce_key = self._get_key('nonce', nonce)
        try:
            del self._request.session[nonce_key]
            return True
        except KeyError:
            return False
