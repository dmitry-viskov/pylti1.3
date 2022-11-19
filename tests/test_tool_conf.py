from .base import TestServicesBase
from .tool_config import get_test_tool_conf


class TestToolConf(TestServicesBase):
    def test_get_jwks(self):
        tc = get_test_tool_conf()
        jwks = tc.get_jwks("https://canvas.instructure.com")
        expected_jwks = {
            "keys": [
                {
                    "e": "AQAB",
                    "kid": "NtQYzsKs_TWLQ0p3bLmfM7fOwY0nEBVVH3z3Q-zJ06Y",
                    "kty": "RSA",
                    "n": "uvEnCaUOy1l9gk3wjW3Pib1dBc5g92-6rhvZZOsN1a77fdOqKsrjWG1lDu8kq2nL-wbAzR3DdEPVw_1WU"
                    "wtr_Q1d5m-7S4ciXT63pENs1EPwWmeN33O0zkGx8I7vdiOTSVoywEyUZe6UyS-ujLfsRc2ImeLP5OHxpE1"
                    "yULEDSiMLtSvgzEaMvf2AkVq5EL5nLYDWXZWXUnpiT_f7iK47Mp2iQd4KYYG7YZ7lMMPCMBuhej7SOtZQ2"
                    "FwaBjvZiXDZ172sQYBCiBAmOR3ofTL6aD2-HUxYztVIPCkhyO84mQ7W4BFsOnKW4WRfEySHXd2hZkFMgcF"
                    "NXY3dA6de519qlcrL0YYx8ZHpzNt0foEzUsgJd8uJMUVvzPZgExwcyIbv5jWYBg0ILgULo7ve7VXG5lMwa"
                    "sW_ch2zKp7tTILnDJwITMjF71h4fn4dMTun_7MWEtSl_iFiALnIL_4_YY717cr4rmcG1424LyxJGRD9L9W"
                    "jO8etAbPkiRFJUd5fmfqjHkO6fPxyWsMUAu8bfYdVRH7qN_erfGHmykmVGgH8AfK9GLT_cjN4GHA29bK9j"
                    "Med6SWdrkygbQmlnsCAHrw0RA-QE0t617h3uTrSEr5vkbLz-KThVEBfH84qsweqcac_unKIZ0e2iRuyVnG"
                    "4cbq8HUdio8gJ62D3wZ0UvVgr4a0",
                    "alg": "RS256",
                    "use": "sig",
                }
            ]
        }
        self.assertEqual(jwks, expected_jwks)

        tc_extended = get_test_tool_conf(tool_conf_extended=True)
        jwks = tc_extended.get_jwks(
            "https://canvas.instructure.com", client_id="10000000000004"
        )
        self.assertEqual(jwks, expected_jwks)
