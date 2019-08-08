from abc import ABCMeta, abstractmethod


class SessionService(object):
    __metaclass__ = ABCMeta
    _session_prefix = 'lti1p3'

    @abstractmethod
    def get_launch_data(self, key):
        raise NotImplemented

    @abstractmethod
    def save_launch_data(self, key, jwt_body):
        raise NotImplemented

    @abstractmethod
    def save_nonce(self, nonce):
        raise NotImplemented

    @abstractmethod
    def check_nonce(self, nonce):
        raise NotImplemented
