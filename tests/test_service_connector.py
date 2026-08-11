# pylint: disable=protected-access
import unittest

from pylti1p3.registration import Registration
from pylti1p3.service_connector import ServiceConnector

SCOPES = [
    "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
    "https://purl.imsglobal.org/spec/lti-ags/scope/score",
]


def _connector(issuer, client_id):
    registration = Registration().set_issuer(issuer).set_client_id(client_id)
    return ServiceConnector(registration)


class TestScopeKey(unittest.TestCase):
    def test_scope_key_differs_by_client_id(self):
        issuer = "https://platform.test"
        first = _connector(issuer, "client-a")._scope_key(SCOPES)
        second = _connector(issuer, "client-b")._scope_key(SCOPES)
        self.assertNotEqual(first, second)

    def test_scope_key_differs_by_issuer(self):
        first = _connector("https://platform.test", "client-a")._scope_key(SCOPES)
        second = _connector("https://other.test", "client-a")._scope_key(SCOPES)
        self.assertNotEqual(first, second)

    def test_scope_key_is_stable_for_the_same_registration(self):
        connector = _connector("https://platform.test", "client-a")
        self.assertEqual(connector._scope_key(SCOPES), connector._scope_key(SCOPES))
