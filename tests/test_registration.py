from pylti1p3.registration import Registration
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAuvEnCaUOy1l9gk3wjW3P
ib1dBc5g92+6rhvZZOsN1a77fdOqKsrjWG1lDu8kq2nL+wbAzR3DdEPVw/1WUwtr
/Q1d5m+7S4ciXT63pENs1EPwWmeN33O0zkGx8I7vdiOTSVoywEyUZe6UyS+ujLfs
Rc2ImeLP5OHxpE1yULEDSiMLtSvgzEaMvf2AkVq5EL5nLYDWXZWXUnpiT/f7iK47
Mp2iQd4KYYG7YZ7lMMPCMBuhej7SOtZQ2FwaBjvZiXDZ172sQYBCiBAmOR3ofTL6
aD2+HUxYztVIPCkhyO84mQ7W4BFsOnKW4WRfEySHXd2hZkFMgcFNXY3dA6de519q
lcrL0YYx8ZHpzNt0foEzUsgJd8uJMUVvzPZgExwcyIbv5jWYBg0ILgULo7ve7VXG
5lMwasW/ch2zKp7tTILnDJwITMjF71h4fn4dMTun/7MWEtSl/iFiALnIL/4/YY71
7cr4rmcG1424LyxJGRD9L9WjO8etAbPkiRFJUd5fmfqjHkO6fPxyWsMUAu8bfYdV
RH7qN/erfGHmykmVGgH8AfK9GLT/cjN4GHA29bK9jMed6SWdrkygbQmlnsCAHrw0
RA+QE0t617h3uTrSEr5vkbLz+KThVEBfH84qsweqcac/unKIZ0e2iRuyVnG4cbq8
HUdio8gJ62D3wZ0UvVgr4a0CAwEAAQ==
-----END PUBLIC KEY-----
"""


class TestRegistrationModel(unittest.TestCase):
    def test_defaults_are_none(self):
        r = Registration()
        self.assertIsNone(r.get_issuer())
        self.assertIsNone(r.get_client_id())
        self.assertIsNone(r.get_key_set_url())
        self.assertIsNone(r.get_auth_token_url())
        self.assertIsNone(r.get_auth_login_url())
        self.assertIsNone(r.get_tool_private_key())

    def test_fluent_setters_return_self(self):
        r = Registration()
        result = (
            r.set_issuer("https://platform.example.com")
            .set_client_id("client-abc")
            .set_auth_token_url("https://platform.example.com/token")
        )
        self.assertIs(result, r)

    def test_setters_and_getters(self):
        r = (
            Registration()
            .set_issuer("https://platform.example.com")
            .set_client_id("client-abc")
            .set_key_set_url("https://platform.example.com/jwks")
            .set_auth_token_url("https://platform.example.com/token")
            .set_auth_login_url("https://platform.example.com/auth")
            .set_auth_audience("https://platform.example.com")
        )
        self.assertEqual(r.get_issuer(), "https://platform.example.com")
        self.assertEqual(r.get_client_id(), "client-abc")
        self.assertEqual(r.get_key_set_url(), "https://platform.example.com/jwks")
        self.assertEqual(r.get_auth_token_url(), "https://platform.example.com/token")
        self.assertEqual(r.get_auth_login_url(), "https://platform.example.com/auth")
        self.assertEqual(r.get_auth_audience(), "https://platform.example.com")

    def test_set_key_set_none(self):
        r = Registration().set_key_set(None)
        self.assertIsNone(r.get_key_set())

    def test_set_key_set_dict(self):
        ks = {"keys": [{"kty": "RSA", "kid": "k1", "alg": "RS256"}]}
        r = Registration().set_key_set(ks)
        self.assertEqual(r.get_key_set(), ks)


class TestRegistrationGetJwk(unittest.TestCase):
    def test_get_jwk_returns_rsa_key(self):
        jwk = Registration.get_jwk(PUBLIC_KEY)
        self.assertEqual(jwk["kty"], "RSA")

    def test_get_jwk_sets_alg_rs256(self):
        jwk = Registration.get_jwk(PUBLIC_KEY)
        self.assertEqual(jwk["alg"], "RS256")

    def test_get_jwk_sets_use_sig(self):
        jwk = Registration.get_jwk(PUBLIC_KEY)
        self.assertEqual(jwk["use"], "sig")

    def test_get_jwk_contains_kid(self):
        jwk = Registration.get_jwk(PUBLIC_KEY)
        self.assertIn("kid", jwk)
        self.assertIsInstance(jwk["kid"], str)

    def test_get_jwks_with_public_key(self):
        r = Registration().set_tool_public_key(PUBLIC_KEY)
        keys = r.get_jwks()
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0]["kty"], "RSA")

    def test_get_jwks_without_public_key_returns_empty(self):
        r = Registration()
        self.assertEqual(r.get_jwks(), [])

    def test_get_kid_with_public_key(self):
        r = Registration().set_tool_public_key(PUBLIC_KEY)
        kid = r.get_kid()
        self.assertIsNotNone(kid)
        self.assertIsInstance(kid, str)

    def test_get_kid_without_public_key_returns_none(self):
        r = Registration()
        self.assertIsNone(r.get_kid())


if __name__ == "__main__":
    unittest.main()
