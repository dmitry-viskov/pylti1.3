from abc import ABCMeta, abstractmethod


class Request(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_request(self, request):
        raise NotImplemented

    @abstractmethod
    def get_param(self, key):
        raise NotImplemented
