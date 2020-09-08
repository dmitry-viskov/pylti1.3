import inspect
import sys
import typing as t
import warnings
from abc import ABCMeta, abstractmethod

REQ = t.TypeVar('REQ', bound='Request')

if t.TYPE_CHECKING:
    from ..request import Request
    from ..registration import Registration
    from ..deployment import Deployment
    from ..message_launch import _LaunchData
    from typing_extensions import Literal, Final
    FIND_REG_KWARGS = t.Union[Literal['oidc_login', 'message_launch'], REQ,
                              _LaunchData]
    PossibleRelationTypes = Literal['one-issuer-one-client-id', 'one-issuer-many-client-ids']


class IssuerToClientRelation(object):
    ONE_CLIENT_ID_PER_ISSUER = 'one-issuer-one-client-id'  # type: Final
    MANY_CLIENTS_IDS_PER_ISSUER = 'one-issuer-many-client-ids'  # type: Final


class ToolConfAbstract(t.Generic[REQ]):
    __metaclass__ = ABCMeta
    reg_extended_search = False  # type: bool
    issuers_relation_types = {}  # type: t.MutableMapping[str, PossibleRelationTypes]

    def __init__(self):
        # type: () -> None
        if sys.version_info[0] > 2:
            argspec = inspect.getfullargspec(self.find_registration_by_issuer)
            self.reg_extended_search = None not in (argspec.varargs, argspec.varkw)
        else:
            argspec = inspect.getargspec(self.find_registration_by_issuer)  # pylint: disable=deprecated-method
            self.reg_extended_search = None not in (argspec.varargs, argspec.keywords)

    def check_iss_has_one_client(self, iss):
        # type: (str) -> bool
        """
        Two methods check_iss_has_one_client / check_iss_has_many_clients are needed for the the backward compatibility
        with the previous versions of the library (1.4.0 and early) where ToolConfDict supported only client_id per iss.
        Should return False for all new ToolConf-s
        """
        iss_type = self.issuers_relation_types.get(iss, IssuerToClientRelation.ONE_CLIENT_ID_PER_ISSUER)
        return iss_type == IssuerToClientRelation.ONE_CLIENT_ID_PER_ISSUER

    def check_iss_has_many_clients(self, iss):
        # type: (str) -> bool
        """
        Should return True for all new ToolConf-s
        """
        iss_type = self.issuers_relation_types.get(iss, IssuerToClientRelation.ONE_CLIENT_ID_PER_ISSUER)
        return iss_type == IssuerToClientRelation.MANY_CLIENTS_IDS_PER_ISSUER

    def set_iss_has_one_client(self, iss):
        # type: (str) -> None
        self.issuers_relation_types[iss] = IssuerToClientRelation.ONE_CLIENT_ID_PER_ISSUER

    def set_iss_has_many_clients(self, iss):
        # type: (str) -> None
        self.issuers_relation_types[iss] = IssuerToClientRelation.MANY_CLIENTS_IDS_PER_ISSUER

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
        """
        Find registration in case if iss has only one client id, i.e
        in case of { ... "iss": { ... "client_id: "client" ... }, ... } config.

        You may skip implementation of this method in case if all iss in your config could have more than one client id.
        """
        raise NotImplementedError

    @abstractmethod
    def find_registration_by_params(self, iss, client_id, *args, **kwargs):
        # type: (str, str, *None, **FIND_REG_KWARGS) -> t.Optional[Registration]
        """
        Find registration in case if iss has many client ids, i.e
        in case of { ... "iss": [ { ... "client_id: "client1" ... }, { ... "client_id: "client2" ... } ], ... } config.

        You may skip implementation of this method in case if all iss in your config couldn't have more than one
        client id, but it is outdated and not recommended way of storing configuration.
        """
        raise NotImplementedError

    @abstractmethod
    def find_deployment(self, iss, deployment_id):
        # type: (str, str) -> t.Optional[Deployment]
        """
        Find deployment in case if iss has only one client id, i.e
        in case of { ... "iss": { ... "client_id: "client" ... }, ... } config.

        You may skip implementation of this method in case if all iss in your config could have more than one client id.
        """
        raise NotImplementedError

    @abstractmethod
    def find_deployment_by_params(self, iss, deployment_id, client_id, *args, **kwargs):
        # type: (str, str, str, *None, **None) -> t.Optional[Deployment]
        """
        Find deployment in case if iss has many client ids, i.e
        in case of { ... "iss": [ { ... "client_id: "client1" ... }, { ... "client_id: "client2" ... } ], ... } config.

        You may skip implementation of this method in case if all iss in your config couldn't have more than one
        client id, but it is outdated and not recommended way of storing configuration.
        """
        raise NotImplementedError

    def get_jwks(self, iss=None, client_id=None, **kwargs):
        keys = []
        if iss:
            if self.check_iss_has_one_client(iss):
                reg = self.find_registration(iss)
            elif self.check_iss_has_many_clients(iss):
                reg = self.find_registration_by_params(iss, client_id, **kwargs)
            else:
                raise Exception('Invalid issuer relation type')
            keys = reg.get_jwks()
        return {
            'keys': keys
        }
