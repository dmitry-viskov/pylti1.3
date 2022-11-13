import typing as t

from .base import LaunchDataStorage

T = t.TypeVar("T")


class CacheDataStorage(LaunchDataStorage[T], t.Generic[T]):
    _cache = None

    def get_session_cookie_name(self) -> t.Optional[str]:
        """
        Workaround for the local non-HTTP usage.
        There is odd situation that all cookies become unavailable from some time
        on the launch step (even if they were set in the new window).
        Looks like it is bug in Chrome >= 80 related to SameSite changes.
        So because of this we have to set all cache values without session prefix.
        It is less secure because if you know unique launch_id you may get access to launch data,
        but unfortunately there is no other way. So please use HTTPS on production :-)
        """
        assert self._request is not None, "Request should be set at this point"
        if not self._request.is_secure():
            return None
        return super().get_session_cookie_name()

    def _get_cache(self):
        assert self._cache is not None, "Cache is not set"
        return self._cache

    def get_value(self, key) -> T:
        key = self._prepare_key(key)
        return self._get_cache().get(key)

    def set_value(self, key: str, value: T, exp: t.Optional[int] = None) -> None:
        key = self._prepare_key(key)
        self._get_cache().set(key, value, exp)

    def check_value(self, key: str) -> bool:
        key = self._prepare_key(key)
        return self._get_cache().get(key) is not None

    def can_set_keys_expiration(self) -> bool:
        return True
