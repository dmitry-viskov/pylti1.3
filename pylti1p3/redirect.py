import typing as t
from abc import ABCMeta, abstractmethod

T = t.TypeVar('T')


class Redirect(t.Generic[T]):
    __metaclass__ = ABCMeta

    @abstractmethod
    def do_redirect(self):
        # type: () -> T
        raise NotImplementedError

    @abstractmethod
    def do_js_redirect(self):
        # type: () -> T
        raise NotImplementedError

    @abstractmethod
    def set_redirect_url(self, location):
        # type: (str) -> None
        raise NotImplementedError

    @abstractmethod
    def get_redirect_url(self):
        # type: () -> str
        raise NotImplementedError
