import typing as t
from abc import ABCMeta, abstractmethod
from ..request import Request

T = t.TypeVar("T")


class LaunchDataStorage(t.Generic[T]):
    __metaclass__ = ABCMeta
    _request: t.Optional[Request] = None
    _session_id: t.Optional[str] = None
    _session_cookie_name: str = "session-id"
    _prefix: str = "lti1p3-"

    def __init__(self, *args, **kwargs) -> None:
        pass

    def set_request(self, request: Request) -> None:
        self._request = request

    def get_session_cookie_name(self) -> t.Optional[str]:
        return self._session_cookie_name

    def get_session_id(self) -> t.Optional[str]:
        return self._session_id

    def set_session_id(self, session_id: str) -> None:
        self._session_id = session_id

    def remove_session_id(self) -> None:
        self._session_id = None

    def _prepare_key(self, key: str) -> str:
        if self._session_id:
            if key.startswith(self._prefix):
                key = key[len(self._prefix) :]
            return self._prefix + self._session_id + "-" + key
        if not key.startswith(self._prefix):
            key = self._prefix + key
        return key

    @abstractmethod
    def can_set_keys_expiration(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_value(self, key: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def set_value(self, key: str, value: T, exp: t.Optional[int] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def check_value(self, key: str) -> bool:
        raise NotImplementedError


class DisableSessionId:
    _session_id: t.Optional[str] = None
    _launch_data_storage: t.Optional[LaunchDataStorage] = None

    def __init__(self, launch_data_storage: t.Optional[LaunchDataStorage]) -> None:
        self._launch_data_storage = launch_data_storage
        if launch_data_storage:
            self._session_id = launch_data_storage.get_session_id()

    def __enter__(self) -> "DisableSessionId":
        if self._launch_data_storage:
            self._launch_data_storage.remove_session_id()
        return self

    def __exit__(self, *args) -> None:
        if self._launch_data_storage and self._session_id:
            self._launch_data_storage.set_session_id(self._session_id)
