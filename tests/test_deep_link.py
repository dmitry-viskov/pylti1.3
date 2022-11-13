from pylti1p3.deep_link_resource import DeepLinkResource
from .base import TestLinkBase
from .django_mixin import DjangoMixin
from .flask_mixin import FlaskMixin


class DeepLinkBase(TestLinkBase):
    # pylint: disable=abstract-method,no-member

    iss = "http://imsglobal.org"
    jwt_canvas_keys = {
        "keys": [
            {
                "kty": "RSA",
                "e": "AQAB",
                "n": "r3WB5ECKptJliYft6F_XJysCy1KevoGJgKNHgdVR20lplUv1SzRH1mifzOmEzxWM0kj6blS"
                "7SRxK9GFGs6optHAmzcb6_joegKzLHSj14RRVSoI0MgyltJcAl8z6d4yZ9KobV8OvpICnMg"
                "sGO20Wih-Cq-oSUjtJT7WET3GZmzmM9MzamiGsCtC0dUWdDOW1FOMzTt8et9YA5jOfkLdJd"
                "PyZ5mdUZjBkYMlDGoD8fPRPdS9M-uczxvUeuKvyy1BVGlu5AG0xy-wN1tKjSE1iuC5Kkm39"
                "CZwQXBRpStDExWw_ApzP40SK3CKez4ls3jjkE3i4CpJSgLn1D8rT6wOpJw",
                "kid": "uhMfBQzVLmaJNU9c1am2X9pTzcEYhgYL2hO6hbYAvdw",
                "alg": "RS256",
                "use": "sig",
            }
        ]
    }

    get_login_data = {
        "iss": iss,
        "login_hint": "DL1",
        "target_link_uri": "http://lti.django.test/launch/",
        "lti_message_hint": "422",
    }

    post_launch_data = {
        "utf8": "%E2%9C%93",
        "state": "state-462a941bbf6a4356afa7",
        "commit": "Perform+Launch",
        "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6InVoTWZCUXpWTG1hSk5VOWMxYW0yWDlwVHpjR"
        "VloZ1lMMmhPNmhiWUF2ZHcifQ.eyJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9"
        "zcGVjL2x0aS9jbGFpbS9tZXNzYWdlX3R5cGUiOiJMdGlEZWVwTGlua2luZ1JlcXVl"
        "c3QiLCJnaXZlbl9uYW1lIjoiTGFxdWl0YSIsImZhbWlseV9uYW1lIjoiSm9obnN0b"
        "24iLCJtaWRkbGVfbmFtZSI6Ikp1bGlhbm4iLCJwaWN0dXJlIjoiaHR0cDovL2V4YW"
        "1wbGUub3JnL0xhcXVpdGEuanBnIiwiZW1haWwiOiJMYXF1aXRhLkpvaG5zdG9uQGV"
        "4YW1wbGUub3JnIiwibmFtZSI6IkxhcXVpdGEgSnVsaWFubiBKb2huc3RvbiIsImh0"
        "dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL3JvbGVzIjpbI"
        "mh0dHA6Ly9wdXJsLmltc2dsb2JhbC5vcmcvdm9jYWIvbGlzL3YyL2luc3RpdHV0aW"
        "9uL3BlcnNvbiNJbnN0cnVjdG9yIl0sImh0dHBzOi8vcHVybC5pbXNnbG9iYWwub3J"
        "nL3NwZWMvbHRpL2NsYWltL3JvbGVfc2NvcGVfbWVudG9yIjpbImE2MmM1MmMwMmJh"
        "MjYyMDAzZjVlIl0sImh0dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL"
        "2NsYWltL2NvbnRleHQiOnsiaWQiOiI0MjIiLCJsYWJlbCI6IlRlc3QgQ291cnNlIi"
        "widGl0bGUiOiJUZXN0IENvdXJzZSIsInR5cGUiOlsiIl19LCJodHRwczovL3B1cmw"
        "uaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS90b29sX3BsYXRmb3JtIjp7Im5h"
        "bWUiOiJMVEkgMS4zIFB5dGhvbiBUZXN0IiwiY29udGFjdF9lbWFpbCI6IiIsImRlc"
        "2NyaXB0aW9uIjoiIiwidXJsIjoiIiwicHJvZHVjdF9mYW1pbHlfY29kZSI6IiIsIn"
        "ZlcnNpb24iOiIxLjAifSwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9"
        "sdGktZGwvY2xhaW0vZGVlcF9saW5raW5nX3NldHRpbmdzIjp7ImFjY2VwdF90eXBl"
        "cyI6WyJsaW5rIiwiZmlsZSIsImh0bWwiLCJsdGlSZXNvdXJjZUxpbmsiLCJpbWFnZ"
        "SJdLCJhY2NlcHRfbWVkaWFfdHlwZXMiOiJpbWFnZS8qLHRleHQvaHRtbCIsImFjY2"
        "VwdF9wcmVzZW50YXRpb25fZG9jdW1lbnRfdGFyZ2V0cyI6WyJpZnJhbWUiLCJ3aW5"
        "kb3ciLCJlbWJlZCJdLCJhY2NlcHRfbXVsdGlwbGUiOnRydWUsImF1dG9fY3JlYXRl"
        "Ijp0cnVlLCJ0aXRsZSI6IlRoaXMgaXMgdGhlIGRlZmF1bHQgdGl0bGUiLCJ0ZXh0I"
        "joiVGhpcyBpcyB0aGUgZGVmYXVsdCB0ZXh0IiwiZGF0YSI6IlNvbWUgcmFuZG9tIG"
        "9wYXF1ZSBkYXRhIHRoYXQgTVVTVCBiZSBzZW50IGJhY2siLCJkZWVwX2xpbmtfcmV"
        "0dXJuX3VybCI6Imh0dHBzOi8vbHRpLXJpLmltc2dsb2JhbC5vcmcvcGxhdGZvcm1z"
        "LzM3MC9jb250ZXh0cy80MjIvZGVlcF9saW5rcyJ9LCJpc3MiOiJodHRwOi8vaW1zZ"
        "2xvYmFsLm9yZyIsImF1ZCI6InB5dGVzdDEyMzQ1IiwiaWF0IjoxNTY1NTM2NDQ0LC"
        "JleHAiOjE1NjU1MzY3NDQsInN1YiI6ImUyOTAzZGEzOTMwZDZjMDllM2MzIiwiaHR"
        "0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGkvY2xhaW0vbHRpMTFfbGVn"
        "YWN5X3VzZXJfaWQiOiJlMjkwM2RhMzkzMGQ2YzA5ZTNjMyIsIm5vbmNlIjoiNDYyY"
        "Tk0MWJiZjZhNDM1NmFmYTciLCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcG"
        "VjL2x0aS9jbGFpbS92ZXJzaW9uIjoiMS4zLjAiLCJsb2NhbGUiOiJlbi1VUyIsImh"
        "0dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL2xhdW5jaF9w"
        "cmVzZW50YXRpb24iOnsiZG9jdW1lbnRfdGFyZ2V0IjoiaWZyYW1lIiwiaGVpZ2h0I"
        "jozMjAsIndpZHRoIjoyNDB9LCJodHRwczovL3d3dy5leGFtcGxlLmNvbS9leHRlbn"
        "Npb24iOnsiY29sb3IiOiJ2aW9sZXQifSwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5"
        "vcmcvc3BlYy9sdGkvY2xhaW0vY3VzdG9tIjp7Im15Q3VzdG9tVmFsdWUiOiIxMjMi"
        "fSwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGkvY2xhaW0vZGVwb"
        "G95bWVudF9pZCI6InB5MTIzNCIsImh0dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3"
        "NwZWMvbHRpL2NsYWltL3RhcmdldF9saW5rX3VyaSI6Imh0dHA6Ly9sdGkuZGphbmd"
        "vLnRlc3QvbGF1bmNoLyJ9.T9YL8HkDU9IOdn7K9QKh-AwHnWHzV9Gu333mFHkvmfY"
        "FFG-gmDu12TzYt7ngRVGzoKiJIDVPvxw1SYWM_SMpjhXuZ6_4QgscCEYR3Fxj5be6"
        "CVhznIEZVUvsN9OWRpn9kvgjdN2gsmQ8eznkVSDn0odZvIyRTiv8-ITAoCpx8Q9GB"
        "ISK6v9pype0QkHfgiwrHwSncOKl4NnoxpQX8VC6QtTKKUP3KEmDaI0g8n6lKbLUx7"
        "KG-BOb7WX19hXtdVbdchhfV79YGlcvLNpDyu7Y1PvYEJqVgV8B5q6Po993YrVRWAB"
        "X17bpJNL2Z9ZGGKL9YV8IgpwrV2p_ADGAjsihyw",
    }

    expected_message_launch_data = {
        "https://purl.imsglobal.org/spec/lti/claim/message_type": "LtiDeepLinkingRequest",
        "given_name": "Laquita",
        "family_name": "Johnston",
        "middle_name": "Juliann",
        "picture": "http://example.org/Laquita.jpg",
        "email": "Laquita.Johnston@example.org",
        "name": "Laquita Juliann Johnston",
        "https://purl.imsglobal.org/spec/lti/claim/roles": [
            "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Instructor"
        ],
        "https://purl.imsglobal.org/spec/lti/claim/role_scope_mentor": [
            "a62c52c02ba262003f5e"
        ],
        "https://purl.imsglobal.org/spec/lti/claim/context": {
            "id": "422",
            "label": "Test Course",
            "title": "Test Course",
            "type": [""],
        },
        "https://purl.imsglobal.org/spec/lti/claim/tool_platform": {
            "name": "LTI 1.3 Python Test",
            "contact_email": "",
            "description": "",
            "url": "",
            "product_family_code": "",
            "version": "1.0",
        },
        "https://purl.imsglobal.org/spec/lti-dl/claim/deep_linking_settings": {
            "accept_types": ["link", "file", "html", "ltiResourceLink", "image"],
            "accept_media_types": "image/*,text/html",
            "accept_presentation_document_targets": ["iframe", "window", "embed"],
            "accept_multiple": True,
            "auto_create": True,
            "title": "This is the default title",
            "text": "This is the default text",
            "data": "Some random opaque data that MUST be sent back",
            "deep_link_return_url": "https://lti-ri.imsglobal.org/platforms/370/contexts/422/deep_links",
        },
        "iss": "http://imsglobal.org",
        "aud": "pytest12345",
        "iat": 1565536444,
        "exp": 1565536744,
        "sub": "e2903da3930d6c09e3c3",
        "https://purl.imsglobal.org/spec/lti/claim/lti11_legacy_user_id": "e2903da3930d6c09e3c3",
        "nonce": "462a941bbf6a4356afa7",
        "https://purl.imsglobal.org/spec/lti/claim/version": "1.3.0",
        "locale": "en-US",
        "https://purl.imsglobal.org/spec/lti/claim/launch_presentation": {
            "document_target": "iframe",
            "height": 320,
            "width": 240,
        },
        "https://www.example.com/extension": {"color": "violet"},
        "https://purl.imsglobal.org/spec/lti/claim/custom": {"myCustomValue": "123"},
        "https://purl.imsglobal.org/spec/lti/claim/deployment_id": "py1234",
        "https://purl.imsglobal.org/spec/lti/claim/target_link_uri": "http://lti.django.test/launch/",
    }

    def test_deep_link_launch_success(self):
        tool_conf, login_request, login_response = self._make_oidc_login(
            uuid_val="462a941bbf6a4356afa7"
        )

        launch_request = self._get_request(login_request, login_response)
        validated_message_launch = self._launch(
            launch_request, tool_conf, force_validation=True
        )
        message_launch_data = validated_message_launch.get_launch_data()
        self.assertDictEqual(message_launch_data, self.expected_message_launch_data)

        resource = DeepLinkResource()
        resource.set_url("http://lti.django.test/launch/").set_custom_params(
            {"custom_param": "custom_value"}
        ).set_title("Test title!")

        deep_link_return_url = message_launch_data.get(
            "https://purl.imsglobal.org/spec/lti-dl/claim/deep_linking_settings"
        ).get("deep_link_return_url")

        html = validated_message_launch.get_deep_link().output_response_form([resource])
        self.assertTrue(
            html.startswith(
                f'<form id="lti13_deep_link_auto_submit" action="{deep_link_return_url}" '
                f'method="POST">'
            )
        )
        self.assertTrue('<input type="hidden" name="JWT" value=' in html)
        self.assertTrue(
            html.endswith(
                '<script type="text/javascript">'
                "document.getElementById('lti13_deep_link_auto_submit').submit();"
                "</script>"
            )
        )


class TestDjangoDeepLink(DjangoMixin, DeepLinkBase):
    pass


class TestFlaskDeepLink(FlaskMixin, DeepLinkBase):
    pass
