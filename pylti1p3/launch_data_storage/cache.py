from .base import LaunchDataStorage


class CacheDataStorage(LaunchDataStorage):
    _cache = None

    def get_session_cookie_name(self):
        """
        Workaround for the local non-HTTP usage.
        There is odd situation that all cookies become unavailable from some time
        on the launch step (even if they were set in the new window).
        Looks like it is bug in Chrome >= 80 related to SameSite changes.
        So because of this we have to set all cache values without session prefix.
        It is less secure because if you know unique launch_id you may get access to launch data,
        but unfortunately there is no other way. So please use HTTPS on production :-)
        """
        if not self._request.is_secure():
            return None
        return super(CacheDataStorage, self).get_session_cookie_name()

    def get_value(self, key):
        key = self._prepare_key(key)
        return self._cache.get(key)

    def set_value(self, key, value, exp=None):
        key = self._prepare_key(key)
        self._cache.set(key, value, exp)

    def check_value(self, key):
        key = self._prepare_key(key)
        return self._cache.get(key) is not None

    def can_set_keys_expiration(self):
        return True
