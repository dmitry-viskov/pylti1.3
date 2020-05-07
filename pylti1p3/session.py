import typing as t
from abc import ABCMeta, abstractmethod

from .launch_data_storage.session import SessionDataStorage

if t.TYPE_CHECKING:
    _JWT_BODY = t.Dict[str, object]
    _STATE_PARAMS = t.Dict[str, object]


class SessionService(object):
    data_storage = None
    _launch_data_lifetime = 86400
    _session_prefix = 'lti1p3'

    def __init__(self, request):
        self.data_storage = SessionDataStorage()
        self.data_storage.set_request(request)

    def _get_key(self, key, nonce=None, add_prefix=True):
        return ((self._session_prefix + '-') if add_prefix else '') + key + (('-' + nonce) if nonce else '')

    def _set_value(self, key, value):
        self.data_storage.set_value(key, value, exp=self._launch_data_lifetime)

    def _get_value(self, key):
        return self.data_storage.get_value(key)

    def get_launch_data(self, key):
        # type: (str) -> _JWT_BODY
        return self._get_value(self._get_key(key, add_prefix=False))

    def save_launch_data(self, key, jwt_body):
        # type: (str, _JWT_BODY) -> None
        self._set_value(self._get_key(key, add_prefix=False), jwt_body)

    def save_nonce(self, nonce):
        # type: (str) -> None
        self._set_value(self._get_key('nonce', nonce), True)

    def check_nonce(self, nonce):
        # type: (str) -> bool
        nonce_key = self._get_key('nonce', nonce)
        return self.data_storage.check_value(nonce_key)

    def save_state_params(self, state, params):
        # type: (str, _STATE_PARAMS) -> None
        self._set_value(self._get_key(state), params)

    def get_state_params(self, state):
        # type: (str) -> _STATE_PARAMS
        return self._get_value(self._get_key(state))

    def set_state_valid(self, state, id_token_hash):
        return self._set_value(self._get_key(state + '-id-token-hash'), id_token_hash)

    def check_state_is_valid(self, state, id_token_hash):
        return self._get_value(self._get_key(state + '-id-token-hash')) == id_token_hash

    def set_data_storage(self, data_storage):
        self.data_storage = data_storage

    def set_launch_data_lifetime(self, time_sec):
        if self.data_storage.can_set_keys_expiration():
            self._launch_data_lifetime = time_sec
        else:
            raise Exception("%s launch storage doesn't support manual change expiration of the keys"
                            % self.data_storage.__class__.__name__)
