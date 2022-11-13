from .base import TestLinkBase
from .django_mixin import DjangoMixin
from .flask_mixin import FlaskMixin


class SubmissionReviewLaunchBase(TestLinkBase):
    # pylint: disable=abstract-method,no-member

    iss = "https://canvas.instructure.com"
    jwt_canvas_keys = {
        "keys": [
            {
                "kty": "RSA",
                "e": "AQAB",
                "n": "wSJ8fSR-ZHfmj00-tQaz2TrOT3TREWIMtfhuNS6JvWFd5kg29TK8y4hBvYi6AMnSWn97Kps"
                "AewK2VABI7MInYRlNRtX9jLrUyatucsOBx4usU2u_qYm3sPpaUgds37mZn1_w6dfbZNG_Z4"
                "givpIUdSAq8QKxCQCk9MV0k94eRMn5xWfJ7hqesb6xiBGKDZUlmt3PfAaSgvk3lxLjd_Jf0"
                "WwZS4KspzjGdeq2ctyuRMB9QZTVvit4PXpRVxT1zwhN3kxH09kWRqNF5CIKw5m93mFmewdC"
                "xjHSZ9AEtTe918zFaYbrh09ZH6E-zz9rXXLvesqoPBDYIT73MeJQhclkqw",
                "kid": "JcJy_-ZbGGXE-fiXLrqbUCyNRg1skGPXngZ5hxD64CA",
                "alg": "RS256",
                "use": "sig",
            }
        ]
    }

    post_login_data = {
        "iss": iss,
        "login_hint": "loginhint",
        "target_link_uri": "http://lti.django.test/launch/",
        "lti_message_hint": "ltimessagehint",
    }

    post_launch_data = {
        "state": "state-test-uuid-1234",
        "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkpjSnlfLVpiR0dYRS1maVhMcnFiVUN5TlJnMXNrR1BYbmdaNWh4R"
        "DY0Q0EifQ.eyJpc3MiOiJodHRwczovL2NhbnZhcy5pbnN0cnVjdHVyZS5jb20iLCJzdWIiOiJhNmQ1YzQ0My0xZjUxLTQ3ODM"
        "tYmExYS03Njg2ZmZlM2I1NGEiLCJhdWQiOiIxMDAwMDAwMDAwMDAwNCIsImV4cCI6MTUxMDE4NTcyOCwiaWF0IjoxNTEwMTg1"
        "MjI4LCJhenAiOiI5NjJmYTRkOC1iY2JmLTQ5YTAtOTRiMi0yZGUwNWFkMjc0YWYiLCJub25jZSI6InRlc3QtdXVpZC0xMjM0I"
        "iwibmFtZSI6Ik1zIEphbmUgTWFyaWUgRG9lIiwiZ2l2ZW5fbmFtZSI6IkphbmUiLCJmYW1pbHlfbmFtZSI6IkRvZSIsImVtYW"
        "lsIjoiamFuZUBleGFtcGxlLm9yZyIsImh0dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL2RlcGxveW1"
        "lbnRfaWQiOiI2Ojg4NjVhYTA1YjRiNzliNjRhOTFhODYwNDJlNDNhZjVlYThhZTc5ZWIiLCJodHRwczovL3B1cmwuaW1zZ2xv"
        "YmFsLm9yZy9zcGVjL2x0aS9jbGFpbS9tZXNzYWdlX3R5cGUiOiJMdGlTdWJtaXNzaW9uUmV2aWV3UmVxdWVzdCIsImh0dHBzO"
        "i8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL3ZlcnNpb24iOiIxLjMuMCIsImh0dHBzOi8vcHVybC5pbXNnbG"
        "9iYWwub3JnL3NwZWMvbHRpL2NsYWltL3JvbGVzIjpbImh0dHA6Ly9wdXJsLmltc2dsb2JhbC5vcmcvdm9jYWIvbGlzL3YyL21"
        "lbWJlcnNoaXAjSW5zdHJ1Y3RvciJdLCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS9jb250ZXh0"
        "Ijp7ImlkIjoiYzFkODg3ZjAtYTFhMy00YmNhLWFlMjUtYzM3NWVkY2MxMzFhIiwibGFiZWwiOiJFQ09OIDEwMTAiLCJ0aXRsZ"
        "SI6IkVjb25vbWljcyBhcyBhIFNvY2lhbCBTY2llbmNlIiwidHlwZSI6WyJDb3Vyc2VPZmZlcmluZyJdfSwiaHR0cHM6Ly9wdX"
        "JsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGktYWdzL2NsYWltL2VuZHBvaW50Ijp7InNjb3BlIjpbImh0dHBzOi8vcHVybC5pbXN"
        "nbG9iYWwub3JnL3NwZWMvbHRpLWFncy9zY29wZS9saW5laXRlbSIsImh0dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMv"
        "bHRpLWFncy9zY29wZS9yZXN1bHQucmVhZG9ubHkiLCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS1hZ3Mvc"
        "2NvcGUvc2NvcmUiXSwibGluZWl0ZW1zIjoiaHR0cHM6Ly93d3cubXl1bml2LmVkdS8yMzQ0L2xpbmVpdGVtcy8iLCJsaW5laX"
        "RlbSI6Imh0dHBzOi8vd3d3Lm15dW5pdi5lZHUvMjM0NC9saW5laXRlbXMvMTIzNC9saW5laXRlbSJ9LCJodHRwczovL3B1cmw"
        "uaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS9mb3JfdXNlciI6eyJ1c2VyX2lkIjoiMTIzOWEtaWx0IiwicGVyc29uX3Nv"
        "dXJjZWRpZCI6ImV4YW1wbGUuZWR1OjcxZWU3ZTQyLWY2ZDItNDE0YS04MGRiLWI2OWFjMmRlZmQ0IiwiZ2l2ZW5fbmFtZSI6I"
        "kp1ZGUiLCJmYW1pbHlfbmFtZSI6IldpbGJlcnQiLCJlbWFpbCI6Imp3aWxiZXJ0QGV4YW1wbGUub3JnIiwicm9sZXMiOlsiaH"
        "R0cDovL3B1cmwuaW1zZ2xvYmFsLm9yZy92b2NhYi9saXMvdjIvbWVtYmVyc2hpcCNMZWFybmVyIl19LCJodHRwczovL3B1cmw"
        "uaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS9yZXNvdXJjZV9saW5rIjp7ImlkIjoiMjAwZDEwMWYtMmMxNC00MzRhLWEw"
        "ZjMtNTdjMmE0MjM2OWZkIiwiZGVzY3JpcHRpb24iOiJBc3NpZ25tZW50IHRvIGludHJvZHVjZSB3aG8geW91IGFyZSIsInRpd"
        "GxlIjoiSW50cm9kdWN0aW9uIEFzc2lnbm1lbnQifSwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGkvY2xhaW"
        "0vbGF1bmNoX3ByZXNlbnRhdGlvbiI6eyJyZXR1cm5fdXJsIjoiaHR0cDovL2V4YW1wbGUub3JnL3JldHVyblRvR3JhZGVib29"
        "rIn0sImh0dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL2N1c3RvbSI6eyJhY3Rpdml0eV9pZCI6IjEy"
        "MyJ9LCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS90b29sX3BsYXRmb3JtIjp7Imd1aWQiOiI4O"
        "TAyMzg5MDIzODo0MzI3MjM4IiwicHJvZHVjdF9mYW1pbHlfY29kZSI6ImV4YW1wbGUub3JnIn19.SKZ1_btZHPx9Avlsh3To4"
        "JZAXb1abZhhlYCubOnJo0rBq-45OhUEdhdMo4rpgsN5TI3lUV7djBaAZv7twnwrGeSw2h7L4zfmlP0pIL8CG5PE1wKqZ3SuuZ"
        "xpt_eHc82ORtNl5wSsKV4ibIKOA1LtPktvCNR3hIv56dbCEscYbxi9sFE8F2YI4KfPhVkcssuew3R1ubUogqCV0Fvn0kCh1EA"
        "tDNgEHcHoEkwLBTd88v3_k-398E6oNEM8HqO5Xef4YFnaFgXeXWh94h2O9L8TctCXAU9P_ZnoV0OVfPF6K8mCf1ES9cMK72UY"
        "CXaaORkicEJPJK3bfLC-d4MZDOb-Aw",
    }

    expected_launch_data = {
        "iss": "https://canvas.instructure.com",
        "sub": "a6d5c443-1f51-4783-ba1a-7686ffe3b54a",
        "aud": "10000000000004",
        "exp": 1510185728,
        "iat": 1510185228,
        "azp": "962fa4d8-bcbf-49a0-94b2-2de05ad274af",
        "nonce": "test-uuid-1234",
        "name": "Ms Jane Marie Doe",
        "given_name": "Jane",
        "family_name": "Doe",
        "email": "jane@example.org",
        "https://purl.imsglobal.org/spec/lti/claim/deployment_id": "6:8865aa05b4b79b64a91a86042e43af5ea8ae79eb",
        "https://purl.imsglobal.org/spec/lti/claim/message_type": "LtiSubmissionReviewRequest",
        "https://purl.imsglobal.org/spec/lti/claim/version": "1.3.0",
        "https://purl.imsglobal.org/spec/lti/claim/roles": [
            "http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor"
        ],
        "https://purl.imsglobal.org/spec/lti/claim/context": {
            "id": "c1d887f0-a1a3-4bca-ae25-c375edcc131a",
            "label": "ECON 1010",
            "title": "Economics as a Social Science",
            "type": ["CourseOffering"],
        },
        "https://purl.imsglobal.org/spec/lti-ags/claim/endpoint": {
            "scope": [
                "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
                "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly",
                "https://purl.imsglobal.org/spec/lti-ags/scope/score",
            ],
            "lineitems": "https://www.myuniv.edu/2344/lineitems/",
            "lineitem": "https://www.myuniv.edu/2344/lineitems/1234/lineitem",
        },
        "https://purl.imsglobal.org/spec/lti/claim/for_user": {
            "user_id": "1239a-ilt",
            "person_sourcedid": "example.edu:71ee7e42-f6d2-414a-80db-b69ac2defd4",
            "given_name": "Jude",
            "family_name": "Wilbert",
            "email": "jwilbert@example.org",
            "roles": ["http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"],
        },
        "https://purl.imsglobal.org/spec/lti/claim/resource_link": {
            "id": "200d101f-2c14-434a-a0f3-57c2a42369fd",
            "description": "Assignment to introduce who you are",
            "title": "Introduction Assignment",
        },
        "https://purl.imsglobal.org/spec/lti/claim/launch_presentation": {
            "return_url": "http://example.org/returnToGradebook"
        },
        "https://purl.imsglobal.org/spec/lti/claim/custom": {"activity_id": "123"},
        "https://purl.imsglobal.org/spec/lti/claim/tool_platform": {
            "guid": "89023890238:4327238",
            "product_family_code": "example.org",
        },
    }

    def test_submission_review_launch_success(self):
        tool_conf, login_request, login_response = self._make_oidc_login()
        launch_request = self._get_request(login_request, login_response)
        validated_message_launch = self._launch(
            launch_request, tool_conf, force_validation=True
        )
        message_launch_data = validated_message_launch.get_launch_data()
        self.assertDictEqual(message_launch_data, self.expected_launch_data)
        self.assertTrue(validated_message_launch.is_submission_review_launch())
        self.assertDictEqual(
            validated_message_launch.get_submission_review_user(),
            self.expected_launch_data.get(
                "https://purl.imsglobal.org/spec/lti/claim/for_user"
            ),
        )


class TestDjangoSubmissionReviewLaunch(DjangoMixin, SubmissionReviewLaunchBase):
    pass


class TestFlaskSubmissionReviewLaunch(FlaskMixin, SubmissionReviewLaunchBase):
    pass
