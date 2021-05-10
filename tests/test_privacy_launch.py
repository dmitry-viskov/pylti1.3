from .base import TestLinkBase
from .django_mixin import DjangoMixin
from .flask_mixin import FlaskMixin


class PrivacyLaunchBase(TestLinkBase):
    # pylint: disable=abstract-method

    iss = 'http://imsglobal.org'
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

    get_login_data = {
        'iss': iss,
        'login_hint': 'PL1',
        'target_link_uri': 'http://lti.django.test/launch/',
        'lti_message_hint': 'LTI_MESSAGE_HINT',
    }

    post_launch_data = {
        'utf8': '%E2%9C%93',
        'state': 'state-6a4356afa7462a941bbf',
        'commit': 'Perform+Launch',
        'id_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkpjSnlfLVpiR0dYRS1maVhMcnFiVUN5TlJnM'
                    'XNrR1BYbmdaNWh4RDY0Q0EifQ.eyJpc3MiOiJodHRwOi8vaW1zZ2xvYmFsLm9yZyI'
                    'sInN1YiI6ImE2ZDVjNDQzLTFmNTEtNDc4My1iYTFhLTc2ODZmZmUzYjU0YSIsImF1'
                    'ZCI6InB5dGVzdDEyMzQ1IiwiZXhwIjoxNTEwMTg1NzI4LCJpYXQiOjE1MTAxODUyM'
                    'jgsIm5vbmNlIjoiNmE0MzU2YWZhNzQ2MmE5NDFiYmYiLCJuYW1lIjoiTXMgSmFuZS'
                    'BNYXJpZSBEb2UiLCJnaXZlbl9uYW1lIjoiSmFuZSIsImZhbWlseV9uYW1lIjoiRG9'
                    'lIiwiZW1haWwiOiJqYW5lQGV4YW1wbGUub3JnIiwiaHR0cHM6Ly9wdXJsLmltc2ds'
                    'b2JhbC5vcmcvc3BlYy9sdGkvY2xhaW0vZGVwbG95bWVudF9pZCI6InB5MTIzNCIsI'
                    'mh0dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL21lc3NhZ2'
                    'VfdHlwZSI6IkRhdGFQcml2YWN5TGF1bmNoUmVxdWVzdCIsImh0dHBzOi8vcHVybC5'
                    'pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL3ZlcnNpb24iOiIxLjMuMCIsImh0'
                    'dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL3JvbGVzIjpbI'
                    'mh0dHA6Ly9wdXJsLmltc2dsb2JhbC5vcmcvdm9jYWIvbGlzL3YyL3N5c3RlbS9wZX'
                    'Jzb24jQWRtaW5pc3RyYXRvciJdLCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9'
                    'zcGVjL2x0aS9jbGFpbS9mb3JfdXNlciI6eyJpZCI6IjhmMDQxZDk0LTk5NDMtNDY2'
                    'Yi05ZGViLWE2OTJhNmI4NWMwMiIsInBlcnNvbl9zb3VyY2VkaWQiOiJleGFtcGxlL'
                    'mVkdTo3MWVlN2U0Mi1mNmQyLTQxNGEtODBkYi1iNjlhYzJkZWZkNCIsImdpdmVuX2'
                    '5hbWUiOiJKdWRlIiwiZmFtaWx5X25hbWUiOiJXaWxiZXJ0IiwiZW1haWwiOiJqd2l'
                    'sYmVydEBleGFtcGxlLm9yZyIsInJvbGVzIjpbImh0dHA6Ly9wdXJsLmltc2dsb2Jh'
                    'bC5vcmcvdm9jYWIvbGlzL3YyL3N5c3RlbS9wZXJzb24jVXNlciJdfSwibG9jYWxlI'
                    'joiZW4tVVMiLCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbG'
                    'FpbS90b29sX3BsYXRmb3JtIjp7Im5hbWUiOiJFeGFtcGxlIFBsYXRmb3JtIiwiZGV'
                    'zY3JpcHRpb24iOiJQcm92aWRlcyBhbiBleGFtcGxlIG9mIGEgcGxhdGZvcm0uIiwi'
                    'Z3VpZCI6IjFiNzYzYThjLTBmOTEtNDYxNS1iYTQ2LWJjM2Q3NzZjYTdmOCIsInByb'
                    '2R1Y3RfZmFtaWx5X2NvZGUiOiJFeGFtcGxlUGxhdGZvcm0iLCJ2ZXJzaW9uIjoiMS'
                    '4wLjAuNiIsInVybCI6Imh0dHBzOi8vcGxhdGZvcm0uZXhhbXBsZS5vcmciLCJjb25'
                    '0YWN0X2VtYWlsIjoic29tZW9uZUBwbGF0Zm9ybS5leGFtcGxlLm9yZyJ9LCJodHRw'
                    'czovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS9jdXN0b20iOnsiU'
                    '29tZV9jdXN0b21fc2V0dGluZyI6ImFfdmFsdWUxIn0sImh0dHBzOi8vcHVybC5pbX'
                    'NnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL2xpcyI6eyJwZXJzb25fc291cmNlZGl'
                    'kIjoiZXhhbXBsZS5lZHU6YjZiOTMxMDUtOGQyZi00YWY4LTkzZWMtMzZjMDUwYjk4'
                    'NDEzIn0sImh0dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL'
                    '2xhdW5jaF9wcmVzZW50YXRpb24iOnsicmV0dXJuX3VybCI6Imh0dHBzOi8vcGxhdG'
                    'Zvcm0uZXhhbXBsZS5vcmcvbHRpL3JldHVybiJ9LCJodHRwczovL3B1cmwuaW1zZ2x'
                    'vYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS90YXJnZXRfbGlua191cmkiOiJodHRwczov'
                    'L3BsYXRmb3JtLmV4YW1wbGUub3JnL2x0aS9wcml2YWN5In0.wE2QG82EG8WUXmC6h'
                    'LwfryE915i_QaMk4fcmVVbSJqyqkH_lbHaIheFX-oVoXHj83PpHpebzXdGAZYkkZf'
                    'nU5HfyMT7dKEmsjmR0z3o36klX-UEZnINqIbapgSJv3Ecfqz4PHG7alc6hbxsjADM'
                    'o9zwclubO1gymfAtxOk3lob1c_j9gmfuB6I2EKLJZUwb4n41yrdpaXuiMEZrlQW6a'
                    'FzCNLVaz9Dnm9H-5-hiLKbUHsmBvGB_MJ_9JEDRKZpgINYdkD9TdNYKDnK-ZSrrmc'
                    'SCC41VgSe1BGcnsz8hgTyPon0Ot3y8bLxXwxuggIKeu0PfVLUnKJUJG8jWNs1dJPA'
    }

    expected_message_launch_data = {
        "iss": "http://imsglobal.org",
        "sub": "a6d5c443-1f51-4783-ba1a-7686ffe3b54a",
        "aud": "pytest12345",
        "exp": 1510185728,
        "iat": 1510185228,
        "nonce": "6a4356afa7462a941bbf",
        "name": "Ms Jane Marie Doe",
        "given_name": "Jane",
        "family_name": "Doe",
        "email": "jane@example.org",
        "https://purl.imsglobal.org/spec/lti/claim/deployment_id": "py1234",
        "https://purl.imsglobal.org/spec/lti/claim/message_type": "DataPrivacyLaunchRequest",
        "https://purl.imsglobal.org/spec/lti/claim/version": "1.3.0",
        "https://purl.imsglobal.org/spec/lti/claim/roles": [
            "http://purl.imsglobal.org/vocab/lis/v2/system/person#Administrator"
        ],
        "https://purl.imsglobal.org/spec/lti/claim/for_user": {
            "id": "8f041d94-9943-466b-9deb-a692a6b85c02",
            "person_sourcedid": "example.edu:71ee7e42-f6d2-414a-80db-b69ac2defd4",
            "given_name": "Jude",
            "family_name": "Wilbert",
            "email": "jwilbert@example.org",
            "roles": ["http://purl.imsglobal.org/vocab/lis/v2/system/person#User"]
        },
        "locale": "en-US",
        "https://purl.imsglobal.org/spec/lti/claim/tool_platform": {
            "name": "Example Platform",
            "description": "Provides an example of a platform.",
            "guid": "1b763a8c-0f91-4615-ba46-bc3d776ca7f8",
            "product_family_code": "ExamplePlatform",
            "version": "1.0.0.6",
            "url": "https://platform.example.org",
            "contact_email": "someone@platform.example.org"
        },
        "https://purl.imsglobal.org/spec/lti/claim/custom": {
            "Some_custom_setting": "a_value1"
        },
        "https://purl.imsglobal.org/spec/lti/claim/lis": {
            "person_sourcedid": "example.edu:b6b93105-8d2f-4af8-93ec-36c050b98413"
        },
        "https://purl.imsglobal.org/spec/lti/claim/launch_presentation": {
            "return_url": "https://platform.example.org/lti/return"
        },
        "https://purl.imsglobal.org/spec/lti/claim/target_link_uri": "https://platform.example.org/lti/privacy"
    }

    def test_privacy_launch_success(self):
        tool_conf, login_request, login_response = self._make_oidc_login(uuid_val='6a4356afa7462a941bbf')
        launch_request = self._get_request(login_request, login_response)
        validated_message_launch = self._launch(launch_request, tool_conf, force_validation=True)
        message_launch_data = validated_message_launch.get_launch_data()
        self.assertDictEqual(message_launch_data, self.expected_message_launch_data)
        self.assertTrue(validated_message_launch.is_data_privacy_launch())


class TestDjangoPrivacyLaunch(DjangoMixin, PrivacyLaunchBase):
    pass


class TestFlaskPrivacyLaunch(FlaskMixin, PrivacyLaunchBase):
    pass
