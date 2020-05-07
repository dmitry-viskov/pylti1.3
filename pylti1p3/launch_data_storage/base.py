from abc import ABCMeta, abstractmethod


class LaunchDataStorage(object):
    __metaclass__ = ABCMeta
    _request = None
    _session_id = None
    _session_cookie_name = 'session-id'
    _prefix = 'lti1p3-'

    def __init__(self, *args, **kwargs):
        pass

    def set_request(self, request):
        self._request = request

    def get_session_cookie_name(self):
        return self._session_cookie_name

    def get_session_id(self):
        return self._session_id

    def set_session_id(self, session_id):
        self._session_id = session_id

    def remove_session_id(self):
        self._session_id = None

    def _prepare_key(self, key):
        if self._session_id:
            if key.startswith(self._prefix):
                key = key[len(self._prefix):]
            return self._prefix + self._session_id + '-' + key
        else:
            if not key.startswith(self._prefix):
                key = self._prefix + key
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


class DisableSessionId(object):
    _session_id = None
    _launch_data_storage = None

    def __init__(self, launch_data_storage):
        self._launch_data_storage = launch_data_storage
        if self._launch_data_storage:
            self._session_id = launch_data_storage.get_session_id()

    def __enter__(self):
        if self._launch_data_storage:
            self._launch_data_storage.remove_session_id()
        return self

    def __exit__(self, *args):
        if self._launch_data_storage:
            self._launch_data_storage.set_session_id(self._session_id)
