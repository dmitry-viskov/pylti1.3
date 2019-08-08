from abc import ABCMeta, abstractmethod


class Redirect(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def do_redirect(self):
        raise NotImplementedError

    @abstractmethod
    def do_js_redirect(self):
        raise NotImplementedError

    @abstractmethod
    def set_redirect_url(self, location):
        raise NotImplementedError

    @abstractmethod
    def get_redirect_url(self):
        raise NotImplementedError
