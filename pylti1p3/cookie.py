from abc import ABCMeta, abstractmethod


class CookieService(object):
    __metaclass__ = ABCMeta
    _cookie_prefix = 'lti1p3'

    @abstractmethod
    def get_cookie(self, name):
        raise NotImplementedError

    @abstractmethod
    def set_cookie(self, name, value, exp=3600):
        raise NotImplementedError
