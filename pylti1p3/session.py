import typing as t
from .launch_data_storage.session import SessionDataStorage
from .request import Request
from .launch_data_storage.base import LaunchDataStorage


TStateParams = t.Dict[str, object]
TJwtBody = t.Mapping[str, t.Any]


class SessionService:
    data_storage: LaunchDataStorage[t.Any]
    _launch_data_lifetime = 86400
    _session_prefix = "lti1p3"

    def __init__(self, request: Request):
        self.data_storage = SessionDataStorage()
        self.data_storage.set_request(request)

    def _get_key(
        self, key: str, nonce: t.Optional[str] = None, add_prefix: bool = True
    ):
        return (
            ((self._session_prefix + "-") if add_prefix else "")
            + key
            + (("-" + nonce) if nonce else "")
        )

    def _set_value(self, key: str, value: object):
        self.data_storage.set_value(key, value, exp=self._launch_data_lifetime)

    def _get_value(self, key: str) -> t.Any:
        return self.data_storage.get_value(key)

    def get_launch_data(self, key: str) -> TJwtBody:
        return self._get_value(self._get_key(key, add_prefix=False))

    def save_launch_data(self, key: str, jwt_body: TJwtBody):
        self._set_value(self._get_key(key, add_prefix=False), jwt_body)

    def save_nonce(self, nonce: str):
        self._set_value(self._get_key("nonce", nonce), True)

    def check_nonce(self, nonce: str) -> bool:
        nonce_key = self._get_key("nonce", nonce)
        return self.data_storage.check_value(nonce_key)

    def save_state_params(self, state: str, params: TStateParams):
        self._set_value(self._get_key(state), params)

    def get_state_params(self, state: str) -> TStateParams:
        return self._get_value(self._get_key(state))

    def set_state_valid(self, state: str, id_token_hash: str):
        return self._set_value(self._get_key(state + "-id-token-hash"), id_token_hash)

    def check_state_is_valid(self, state: str, id_token_hash: str) -> bool:
        return self._get_value(self._get_key(state + "-id-token-hash")) == id_token_hash

    def set_data_storage(self, data_storage: LaunchDataStorage[t.Any]):
        self.data_storage = data_storage

    def set_launch_data_lifetime(self, time_sec: int):
        if self.data_storage.can_set_keys_expiration():
            self._launch_data_lifetime = time_sec
        else:
            raise Exception(
                f"{self.data_storage.__class__.__name__} launch storage doesn't support "
                f"manual change expiration of the keys"
            )
