import typing as t
from abc import ABCMeta, abstractmethod

if t.TYPE_CHECKING:
    from typing_extensions import Protocol

    class SessionLike(Protocol):
        @t.overload
        def get(self, key):
            # type: (str) -> t.Any
            pass

        @t.overload
        def get(self, key, default):  # pylint: disable=function-redefined
            # type: (str, t.Any) -> t.Any
            pass

        def get(self, key, default=None):  # pylint: disable=function-redefined
            # type: (str, t.Any) -> t.Any
            pass

        def __setitem__(self, key, value):
            # type: (str, t.Any) -> None
            pass

        def __contains__(self, key):
            # type: (object) -> bool
            pass


class Request(object):
    __metaclass__ = ABCMeta

    @property
    def session(self):
        # type: () -> SessionLike
        raise NotImplementedError

    @abstractmethod
    def is_secure(self):
        # type: () -> bool
        raise NotImplementedError

    @abstractmethod
    def get_param(self, key):
        # type: (str) -> object
        raise NotImplementedError
