from abc import ABCMeta, abstractmethod


class ToolConfAbstract(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def find_registration_by_issuer(self, iss):
        raise NotImplementedError

    @abstractmethod
    def find_deployment(self, iss, deployment_id):
        raise NotImplementedError
