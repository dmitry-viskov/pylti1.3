import inspect
import sys
import warnings
from abc import ABCMeta, abstractmethod


class IssuerToClientRelation(object):
    ONE_CLIENT_ID_PER_ISSUER = 'one-issuer-one-client-id'
    MANY_CLIENTS_IDS_PER_ISSUER = 'one-issuer-many-client-ids'


class ToolConfAbstract(object):
    __metaclass__ = ABCMeta
    reg_extended_search = False
    issuers_relation_types = {}

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
        """
        Find registration in case if iss has only one client id, i.e
        in case of { ... "iss": { ... "client_id: "client" ... }, ... } config
        """
        raise NotImplementedError

    @abstractmethod
    def find_registration_by_params(self, iss, client_id, *args, **kwargs):
        """
        Find registration in case if iss has many client ids, i.e
        in case of { ... "iss": [ { ... "client_id: "client1" ... }, { ... "client_id: "client2" ... } ], ... } config
        """
        raise NotImplementedError

    @abstractmethod
    def find_deployment(self, iss, deployment_id):
        """
        Find deployment in case if iss has only one client id, i.e
        in case of { ... "iss": { ... "client_id: "client" ... }, ... } config
        """
        raise NotImplementedError

    @abstractmethod
    def find_deployment_by_params(self, iss, deployment_id, client_id, *args, **kwargs):
        """
        Find deployment in case if iss has many client ids, i.e
        in case of { ... "iss": [ { ... "client_id: "client1" ... }, { ... "client_id: "client2" ... } ], ... } config
        """
        raise NotImplementedError

    def set_iss_has_one_client(self, iss):
        self.issuers_relation_types[iss] = IssuerToClientRelation.ONE_CLIENT_ID_PER_ISSUER

    def set_iss_has_many_clients(self, iss):
        self.issuers_relation_types[iss] = IssuerToClientRelation.MANY_CLIENTS_IDS_PER_ISSUER

    def check_iss_has_one_client(self, iss):
        iss_type = self.issuers_relation_types.get(iss, IssuerToClientRelation.ONE_CLIENT_ID_PER_ISSUER)
        return iss_type == IssuerToClientRelation.ONE_CLIENT_ID_PER_ISSUER

    def check_iss_has_many_clients(self, iss):
        iss_type = self.issuers_relation_types.get(iss, IssuerToClientRelation.ONE_CLIENT_ID_PER_ISSUER)
        return iss_type == IssuerToClientRelation.MANY_CLIENTS_IDS_PER_ISSUER

    def get_jwks(self, iss, client_id=None, **kwargs):
        if self.check_iss_has_one_client(iss):
            reg = self.find_registration(iss)
        elif self.check_iss_has_many_clients(iss):
            reg = self.find_registration_by_params(iss, client_id, **kwargs)
        else:
            raise Exception('Invalid issuer relation type')
        return {
            'keys': reg.get_jwks()
        }
