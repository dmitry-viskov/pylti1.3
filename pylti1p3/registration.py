import json
from jwcrypto.jwk import JWK


class Registration(object):
    _issuer = None
    _client_id = None
    _key_set_url = None
    _key_set = None
    _auth_token_url = None
    _auth_login_url = None
    _auth_audience = None
    _tool_private_key = None
    _tool_public_key = None

    def get_issuer(self):
        return self._issuer

    def set_issuer(self, issuer):
        self._issuer = issuer
        return self

    def get_client_id(self):
        return self._client_id

    def set_client_id(self, client_id):
        self._client_id = client_id
        return self

    def get_key_set(self):
        return self._key_set

    def set_key_set(self, key_set):
        self._key_set = key_set
        return self

    def get_key_set_url(self):
        return self._key_set_url

    def set_key_set_url(self, key_set_url):
        self._key_set_url = key_set_url
        return self

    def get_auth_token_url(self):
        return self._auth_token_url

    def set_auth_token_url(self, auth_token_url):
        self._auth_token_url = auth_token_url
        return self

    def get_auth_login_url(self):
        return self._auth_login_url

    def set_auth_login_url(self, auth_login_url):
        self._auth_login_url = auth_login_url
        return self

    def get_auth_audience(self):
        return self._auth_audience

    def set_auth_audience(self, auth_audience):
        self._auth_audience = auth_audience
        return self

    def get_tool_private_key(self):
        return self._tool_private_key

    def set_tool_private_key(self, tool_private_key):
        self._tool_private_key = tool_private_key
        return self

    def get_tool_public_key(self):
        return self._tool_public_key

    def set_tool_public_key(self, tool_public_key):
        self._tool_public_key = tool_public_key
        return self

    @classmethod
    def get_jwk(cls, public_key):
        jwk_obj = JWK.from_pem(public_key.encode('utf-8'))
        public_jwk = json.loads(jwk_obj.export_public())
        public_jwk['alg'] = 'RS256'
        public_jwk['use'] = 'sig'
        return public_jwk

    def get_jwks(self):
        keys = []
        public_key = self.get_tool_public_key()
        if public_key:
            keys.append(Registration.get_jwk(public_key))
        return keys

    def get_kid(self):
        key = self.get_tool_public_key()
        if key:
            jwk = Registration.get_jwk(key)
            return jwk.get('kid') if jwk else None
        return None
