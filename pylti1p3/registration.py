import json
import typing as t

from jwcrypto.jwk import JWK  # type: ignore

T_SELF = t.TypeVar('T_SELF', bound='Registration')


if t.TYPE_CHECKING:
    from mypy_extensions import TypedDict
    _Key = TypedDict('_Key', {'kid': str, 'alg': str}, total=True)
    _KeySet = TypedDict('_KeySet', {'keys': t.List[_Key]}, total=True)
    from cryptography.hazmat.primitives.asymmetric.rsa import (
        RSAPublicKey, RSAPrivateKey
    )
    _POSSIBLE_KEYS = t.Union[str, bytes, RSAPrivateKey, RSAPublicKey]


class Registration(object):
    _issuer = None  # type: t.Optional[str]
    _client_id = None  # type: t.Optional[str]
    _key_set_url = None  # type: t.Optional[str]
    _key_set = None  # type: t.Optional[_KeySet]
    _auth_token_url = None  # type: t.Optional[str]
    _auth_login_url = None  # type: t.Optional[str]
    _tool_private_key = None  # type: t.Optional[_POSSIBLE_KEYS]
    _auth_audience = None
    _tool_public_key = None

    def get_issuer(self):
        # type: () -> t.Optional[str]
        return self._issuer

    def set_issuer(self, issuer):
        # type: (T_SELF, str) -> T_SELF
        self._issuer = issuer
        return self

    def get_client_id(self):
        # type: () -> t.Optional[str]
        return self._client_id

    def set_client_id(self, client_id):
        # type: (T_SELF, str) -> T_SELF
        self._client_id = client_id
        return self

    def get_key_set(self):
        # type: () -> t.Optional[_KeySet]
        return self._key_set

    def set_key_set(self, key_set):
        # type: (T_SELF, t.Optional[_KeySet]) -> T_SELF
        self._key_set = key_set
        return self

    def get_key_set_url(self):
        # type: () -> t.Optional[str]
        return self._key_set_url

    def set_key_set_url(self, key_set_url):
        # type: (T_SELF, str) -> T_SELF
        self._key_set_url = key_set_url
        return self

    def get_auth_token_url(self):
        # type: () -> t.Optional[str]
        return self._auth_token_url

    def set_auth_token_url(self, auth_token_url):
        # type: (T_SELF, str) -> T_SELF
        self._auth_token_url = auth_token_url
        return self

    def get_auth_login_url(self):
        # type: () -> t.Optional[str]
        return self._auth_login_url

    def set_auth_login_url(self, auth_login_url):
        # type: (T_SELF, str) -> T_SELF
        self._auth_login_url = auth_login_url
        return self

    def get_auth_audience(self):
        return self._auth_audience

    def set_auth_audience(self, auth_audience):
        self._auth_audience = auth_audience
        return self

    def get_tool_private_key(self):
        # type: () -> t.Optional[_POSSIBLE_KEYS]
        return self._tool_private_key

    def set_tool_private_key(self, tool_private_key):
        # type: (T_SELF, _POSSIBLE_KEYS) -> T_SELF
        self._tool_private_key = tool_private_key
        return self

    def get_tool_public_key(self):
        return self._tool_public_key

    def set_tool_public_key(self, tool_public_key):
        self._tool_public_key = tool_public_key
        return self

    @classmethod
    def get_jwk(cls, public_key):
        # type: (str) -> t.Mapping[str, t.Any]
        jwk_obj = JWK.from_pem(public_key.encode('utf-8'))
        public_jwk = json.loads(jwk_obj.export_public())
        public_jwk['alg'] = 'RS256'
        public_jwk['use'] = 'sig'
        return public_jwk

    def get_jwks(self):
        # type: () -> t.List[t.Mapping[str, t.Any]]
        keys = []
        public_key = self.get_tool_public_key()
        if public_key:
            keys.append(Registration.get_jwk(public_key))
        return keys

    def get_kid(self):
        # type: () -> t.Optional[str]
        key = self.get_tool_public_key()
        if key:
            jwk = Registration.get_jwk(key)
            return jwk.get('kid') if jwk else None
        return None
