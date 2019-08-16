from abc import ABCMeta, abstractmethod


class SessionService(object):
    __metaclass__ = ABCMeta
    _session_prefix = 'lti1p3'

    @abstractmethod
    def get_launch_data(self, key):
        raise NotImplementedError

    @abstractmethod
    def save_launch_data(self, key, jwt_body):
        raise NotImplementedError

    @abstractmethod
    def save_nonce(self, nonce):
        raise NotImplementedError

    @abstractmethod
    def check_nonce(self, nonce):
        raise NotImplementedError

    @abstractmethod
    def save_state_params(self, state, params):
        raise NotImplementedError

    @abstractmethod
    def get_state_params(self, state):
        raise NotImplementedError
