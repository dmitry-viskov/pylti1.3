import typing as t
from abc import ABCMeta, abstractmethod

T = t.TypeVar('T')


class Request(t.Generic[T]):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_request(self, request):
        # type: (T) -> None
        raise NotImplementedError

    @abstractmethod
    def get_param(self, key):
        # type: (str) -> object
        raise NotImplementedError
