import json
import typing as t
import typing_extensions as te
from jwcrypto.jwk import JWK  # type: ignore


TKey = te.TypedDict("TKey", {"kid": str, "alg": str}, total=True)
TKeySet = te.TypedDict("TKeySet", {"keys": t.List[TKey]}, total=True)


class Registration:
    _issuer: t.Optional[str] = None
    _client_id: t.Optional[str] = None
    _key_set_url: t.Optional[str] = None
    _key_set: t.Optional[TKeySet] = None
    _auth_token_url: t.Optional[str] = None
    _auth_login_url: t.Optional[str] = None
    _tool_private_key: t.Optional[str] = None
    _auth_audience: t.Optional[str] = None
    _tool_public_key = None

    def get_issuer(self) -> t.Optional[str]:
        return self._issuer

    def set_issuer(self, issuer: str) -> "Registration":
        self._issuer = issuer
        return self

    def get_client_id(self) -> t.Optional[str]:
        return self._client_id

    def set_client_id(self, client_id: str) -> "Registration":
        self._client_id = client_id
        return self

    def get_key_set(self) -> t.Optional[TKeySet]:
        return self._key_set

    def set_key_set(self, key_set: t.Optional[TKeySet]) -> "Registration":
        self._key_set = key_set
        return self

    def get_key_set_url(self) -> t.Optional[str]:
        return self._key_set_url

    def set_key_set_url(self, key_set_url: t.Optional[str]) -> "Registration":
        self._key_set_url = key_set_url
        return self

    def get_auth_token_url(self) -> t.Optional[str]:
        return self._auth_token_url

    def set_auth_token_url(self, auth_token_url: str) -> "Registration":
        self._auth_token_url = auth_token_url
        return self

    def get_auth_login_url(self) -> t.Optional[str]:
        return self._auth_login_url

    def set_auth_login_url(self, auth_login_url: str) -> "Registration":
        self._auth_login_url = auth_login_url
        return self

    def get_auth_audience(self) -> t.Optional[str]:
        return self._auth_audience

    def set_auth_audience(self, auth_audience: str) -> "Registration":
        self._auth_audience = auth_audience
        return self

    def get_tool_private_key(self) -> t.Optional[str]:
        return self._tool_private_key

    def set_tool_private_key(self, tool_private_key: str) -> "Registration":
        self._tool_private_key = tool_private_key
        return self

    def get_tool_public_key(self):
        return self._tool_public_key

    def set_tool_public_key(self, tool_public_key) -> "Registration":
        self._tool_public_key = tool_public_key
        return self

    @classmethod
    def get_jwk(cls, public_key: str) -> t.Mapping[str, t.Any]:
        jwk_obj = JWK.from_pem(public_key.encode("utf-8"))
        public_jwk = json.loads(jwk_obj.export_public())
        public_jwk["alg"] = "RS256"
        public_jwk["use"] = "sig"
        return public_jwk

    def get_jwks(self) -> t.List[t.Mapping[str, t.Any]]:
        keys = []
        public_key = self.get_tool_public_key()
        if public_key:
            keys.append(Registration.get_jwk(public_key))
        return keys

    def get_kid(self) -> t.Optional[str]:
        key = self.get_tool_public_key()
        if key:
            jwk = Registration.get_jwk(key)
            return jwk.get("kid") if jwk else None
        return None
