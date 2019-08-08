from abc import ABCMeta, abstractmethod


class Redirect(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def do_redirect(self):
        raise NotImplemented

    @abstractmethod
    def do_js_redirect(self):
        raise NotImplemented

    @abstractmethod
    def set_redirect_url(self, location):
        raise NotImplemented

    @abstractmethod
    def get_redirect_url(self):
        raise NotImplemented
