from abc import ABCMeta, abstractmethod


class Request(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_param(self, key):
        raise NotImplementedError
