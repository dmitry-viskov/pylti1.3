from abc import ABCMeta, abstractmethod


class Request:
    __metaclass__ = ABCMeta

    @property
    def session(self):
        raise NotImplementedError

    @abstractmethod
    def is_secure(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_param(self, key: str) -> str:
        raise NotImplementedError
