from abc import ABCMeta, abstractmethod


class LaunchDataStorage(object):
    __metaclass__ = ABCMeta
    _request = None
    _session_id = None
    _session_cookie_name = 'session-id'

    def __init__(self, *args, **kwargs):
        pass

    def set_request(self, request):
        self._request = request

    def get_session_cookie_name(self):
        return self._session_cookie_name

    def set_session_id(self, session_id):
        self._session_id = session_id

    def _prepare_key(self, key):
        if self._session_id:
            return 'lti1p3-' + self._session_id + '-' + key
        else:
            return key

    @abstractmethod
    def can_set_keys_expiration(self):
        raise NotImplementedError

    @abstractmethod
    def get_value(self, key):
        raise NotImplementedError

    @abstractmethod
    def set_value(self, key, value, exp=None):
        raise NotImplementedError

    @abstractmethod
    def check_value(self, key):
        raise NotImplementedError
