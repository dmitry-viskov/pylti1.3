import typing as t
from abc import ABCMeta, abstractmethod

if t.TYPE_CHECKING:
    _JWT_BODY = t.Dict[str, object]
    _STATE_PARAMS = t.Dict[str, object]


class SessionService(object):
    __metaclass__ = ABCMeta
    _session_prefix = 'lti1p3'

    @abstractmethod
    def get_launch_data(self, key):
        # type: (str) -> _JWT_BODY
        raise NotImplementedError

    @abstractmethod
    def save_launch_data(self, key, jwt_body):
        # type: (str, _JWT_BODY) -> None
        raise NotImplementedError

    @abstractmethod
    def save_nonce(self, nonce):
        # type: (str) -> None
        raise NotImplementedError

    @abstractmethod
    def check_nonce(self, nonce):
        # type: (str) -> bool
        raise NotImplementedError

    @abstractmethod
    def save_state_params(self, state, params):
        # type: (str, _STATE_PARAMS) -> None
        raise NotImplementedError

    @abstractmethod
    def get_state_params(self, state):
        # type: (str) -> _STATE_PARAMS
        raise NotImplementedError
