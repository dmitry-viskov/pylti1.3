from .base import LaunchDataStorage


class SessionDataStorage(LaunchDataStorage):

    def get_session_cookie_name(self):
        return None

    def set_session_id(self, session_id):
        pass

    def get_value(self, key):
        return self._request.session.get(key, None)

    def set_value(self, key, value, exp=None):
        self._request.session[key] = value

    def check_value(self, key):
        return key in self._request.session

    def can_set_keys_expiration(self):
        return False
