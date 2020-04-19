import inspect
import sys
import warnings
from abc import ABCMeta, abstractmethod
from .mode import ToolConfMode


class ToolConfAbstract(object):
    __metaclass__ = ABCMeta
    reg_extended_search = False
    mode = ToolConfMode.ONE_ISSUER_ONE_CLIENT_ID

    def __init__(self):
        if sys.version_info[0] > 2:
            argspec = inspect.getfullargspec(self.find_registration_by_issuer)
            self.reg_extended_search = None not in (argspec.varargs, argspec.varkw)
        else:
            argspec = inspect.getargspec(self.find_registration_by_issuer)  # pylint: disable=deprecated-method
            self.reg_extended_search = None not in (argspec.varargs, argspec.keywords)

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
    def find_registration_by_params(self, iss, client_id, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def find_deployment(self, iss, deployment_id):
        raise NotImplementedError

    @abstractmethod
    def find_deployment_by_params(self, iss, deployment_id, client_id, *args, **kwargs):
        raise NotImplementedError

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        if self.mode not in (ToolConfMode.ONE_ISSUER_ONE_CLIENT_ID, ToolConfMode.ONE_ISSUER_MANY_CLIENT_IDS):
            raise Exception('Invalid mode')
        return self.mode

    def check_mode(self, mode):
        return self.mode == mode

    def get_jwks(self, iss, client_id=None, **kwargs):
        if self.mode == ToolConfMode.ONE_ISSUER_ONE_CLIENT_ID:
            reg = self.find_registration(iss, client_id=client_id)
        elif self.mode == ToolConfMode.ONE_ISSUER_MANY_CLIENT_IDS:
            reg = self.find_registration_by_params(iss, client_id, **kwargs)
        else:
            raise Exception('Invalid mode')
        return {
            'keys': reg.get_jwks()
        }
