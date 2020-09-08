import typing as t
from abc import ABCMeta, abstractmethod

if t.TYPE_CHECKING:
    from ..request import Request

_T_DISABLED_SESSION_ID = t.TypeVar('_T_DISABLED_SESSION_ID', bound='DisableSessionId')
T = t.TypeVar('T')


class LaunchDataStorage(t.Generic[T]):
    __metaclass__ = ABCMeta
    _request = None  # type: t.Optional[Request]
    _session_id = None  # type: t.Optional[str]
    _session_cookie_name = 'session-id'  # type: str
    _prefix = 'lti1p3-'  # type: str

    def __init__(self, *args, **kwargs):
        # type: (*t.Any, **t.Any) -> None
        pass

    def set_request(self, request):
        # type: (Request) -> None
        self._request = request

    def get_session_cookie_name(self):
        # type: () -> t.Optional[str]
        return self._session_cookie_name

    def get_session_id(self):
        # type: () -> t.Optional[str]
        return self._session_id

    def set_session_id(self, session_id):
        # type: (str) -> None
        self._session_id = session_id

    def remove_session_id(self):
        # type: () -> None
        self._session_id = None

    def _prepare_key(self, key):
        # type: (str) -> str
        if self._session_id:
            if key.startswith(self._prefix):
                key = key[len(self._prefix):]
            return self._prefix + self._session_id + '-' + key
        else:
            if not key.startswith(self._prefix):
                key = self._prefix + key
            return key

    @abstractmethod
    def can_set_keys_expiration(self):
        # type: () -> bool
        raise NotImplementedError

    @abstractmethod
    def get_value(self, key):
        # type: (str) -> T
        raise NotImplementedError

    @abstractmethod
    def set_value(self, key, value, exp=None):
        # type: (str, T, t.Optional[int]) -> None
        raise NotImplementedError

    @abstractmethod
    def check_value(self, key):
        # type: (str) -> bool
        raise NotImplementedError


class DisableSessionId(object):
    _session_id = None  # type: t.Optional[str]
    _launch_data_storage = None  # type: t.Optional[LaunchDataStorage]

    def __init__(self, launch_data_storage):
        # type: (t.Optional[LaunchDataStorage]) -> None
        self._launch_data_storage = launch_data_storage
        if launch_data_storage:
            self._session_id = launch_data_storage.get_session_id()

    def __enter__(self):
        # type: (_T_DISABLED_SESSION_ID) -> _T_DISABLED_SESSION_ID
        if self._launch_data_storage:
            self._launch_data_storage.remove_session_id()
        return self

    def __exit__(self, *args):
        # type: (*t.Any) -> None
        if self._launch_data_storage and self._session_id:
            self._launch_data_storage.set_session_id(self._session_id)
