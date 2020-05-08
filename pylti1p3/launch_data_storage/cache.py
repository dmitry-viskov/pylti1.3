import typing as t

from .base import LaunchDataStorage

T = t.TypeVar('T')


class CacheDataStorage(LaunchDataStorage[T], t.Generic[T]):
    # This seems a bit strange, I have no idea when this is ever set.
    _cache = None  # type: t.Any

    def get_session_cookie_name(self):
        # type: () -> t.Optional[str]
        """
        Workaround for the local non-HTTP usage.
        There is odd situation that all cookies become unavailable from some time
        on the launch step (even if they were set in the new window).
        Looks like it is bug in Chrome >= 80 related to SameSite changes.
        So because of this we have to set all cache values without session prefix.
        It is less secure because if you know unique launch_id you may get access to launch data,
        but unfortunately there is no other way. So please use HTTPS on production :-)
        """
        assert self._request is not None, 'Request should be set at this point'
        if not self._request.is_secure():
            return None
        return super(CacheDataStorage, self).get_session_cookie_name()

    def get_value(self, key):
        # type: (str) -> T
        key = self._prepare_key(key)
        return self._cache.get(key)

    def set_value(self, key, value, exp=None):
        # type: (str, T, t.Optional[int]) -> None
        key = self._prepare_key(key)
        self._cache.set(key, value, exp)

    def check_value(self, key):
        # type: (str) -> bool
        key = self._prepare_key(key)
        return self._cache.get(key) is not None

    def can_set_keys_expiration(self):
        # type: () -> bool
        return True
