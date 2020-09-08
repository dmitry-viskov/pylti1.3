import typing as t

from .base import LaunchDataStorage

T = t.TypeVar('T')


class SessionDataStorage(LaunchDataStorage[T], t.Generic[T]):
    def get_session_cookie_name(self):
        # type: () -> None
        return None

    def set_session_id(self, session_id):
        # type: (str) -> None
        pass

    def get_value(self, key):
        # type: (str) -> T
        assert self._request is not None, 'Request should be set at this point'
        return self._request.session.get(key, None)

    def set_value(self, key, value, exp=None):
        # type: (str, T, t.Optional[int]) -> None
        # pylint: disable=unused-argument
        assert self._request is not None, 'Request should be set at this point'
        self._request.session[key] = value

    def check_value(self, key):
        # type: (str) -> bool
        assert self._request is not None, 'Request should be set at this point'
        return key in self._request.session

    def can_set_keys_expiration(self):
        # type: () -> bool
        return False
