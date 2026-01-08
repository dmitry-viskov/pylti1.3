import typing as t
from abc import ABCMeta, abstractmethod


class CookieService:
    __metaclass__ = ABCMeta
    _cookie_prefix: str = "lti1p3"

    @abstractmethod
    def get_cookie(self, name: str) -> t.Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def set_cookie(
        self, name: str, value: t.Union[str, int], exp: t.Optional[int] = 3600
    ):
        raise NotImplementedError
