import typing as t
from abc import ABCMeta, abstractmethod


class CookieService(object):
    __metaclass__ = ABCMeta
    _cookie_prefix = 'lti1p3'  # type: str

    @abstractmethod
    def get_cookie(self, name):
        # type: (str) -> t.Optional[str]
        raise NotImplementedError

    @abstractmethod
    def set_cookie(self, name, value, exp=3600):
        # type: (str, str, int) -> None
        raise NotImplementedError
