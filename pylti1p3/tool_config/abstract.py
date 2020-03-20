import inspect
import sys
import typing as t
import warnings
from abc import ABCMeta, abstractmethod

from ..actions import Action

REQ = t.TypeVar('REQ', bound='Request')

if t.TYPE_CHECKING:
    from ..request import Request
    from ..registration import Registration
    from ..deployment import Deployment
    from ..message_launch import _LaunchData
    from typing_extensions import Literal
    FIND_REG_KWARGS = t.Union[Literal['oidc_login', 'message_launch'], REQ,
                              _LaunchData]


class ToolConfAbstract(t.Generic[REQ]):
    __metaclass__ = ABCMeta
    reg_extended_search = False

    def __init__(self):
        # type: () -> None
        if sys.version_info[0] > 2:
            argspec = inspect.getfullargspec(self.find_registration_by_issuer)
            self.reg_extended_search = None not in (argspec.varargs,
                                                    argspec.varkw)
        else:
            argspec = inspect.getargspec(self.find_registration_by_issuer)  # pylint: disable=deprecated-method
            self.reg_extended_search = None not in (argspec.varargs,
                                                    argspec.keywords)

    def find_registration(self, iss, *args, **kwargs):
        # type: (str, *None, **FIND_REG_KWARGS) -> t.Optional[Registration]
        if self.reg_extended_search:
            return self.find_registration_by_issuer(iss, *args, **kwargs)
        else:
            warnings.warn(
                "Signature of ToolConfAbstract.find_registration_by_issuer method was changed, "
                "please update you custom implementation", DeprecationWarning)
            return self.find_registration_by_issuer(iss)

    @abstractmethod
    def find_registration_by_issuer(self, iss, *args, **kwargs):
        # type: (str, *None, **FIND_REG_KWARGS) -> t.Optional[Registration]
        raise NotImplementedError

    @abstractmethod
    def find_deployment(self, iss, deployment_id, get_param):
        # type: (str, str, t.Callable[[str], object]) -> t.Optional[Deployment]
        raise NotImplementedError
