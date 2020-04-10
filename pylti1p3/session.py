from .launch_data_storage.session import SessionDataStorage


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
        return self._get_value(self._get_key(key, add_prefix=False))

    def save_launch_data(self, key, jwt_body):
        self._set_value(self._get_key(key, add_prefix=False), jwt_body)

    def save_nonce(self, nonce):
        self._set_value(self._get_key('nonce', nonce), True)

    def check_nonce(self, nonce):
        nonce_key = self._get_key('nonce', nonce)
        return self.data_storage.check_value(nonce_key)

    def save_state_params(self, state, params):
        self._set_value(self._get_key(state), params)

    def get_state_params(self, state):
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
