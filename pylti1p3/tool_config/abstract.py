import warnings
from abc import ABCMeta, abstractmethod


class ToolConfAbstract(object):
    __metaclass__ = ABCMeta
    reg_extended_search = False

    def __init__(self):
        co_varnames = self.find_registration_by_issuer.__code__.co_varnames
        self.reg_extended_search = all([arg in co_varnames for arg in ('args', 'kwargs')])

    def find_registration(self, iss, *args, **kwargs):
        if self.reg_extended_search:
            return self.find_registration_by_issuer(iss, *args, **kwargs)
        else:
            warnings.warn("Signature of ToolConfAbstract.find_registration_by_issuer method was changed, "
                          "please update you custom implementation",
                          DeprecationWarning)
            return self.find_registration_by_issuer(iss)

    @abstractmethod
    def find_registration_by_issuer(self, iss, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def find_deployment(self, iss, deployment_id):
        raise NotImplementedError
