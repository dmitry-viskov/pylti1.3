from .base import TestLinkBase
from .django_mixin import DjangoMixin
from .flask_mixin import FlaskMixin


class PrivacyLaunchBase(TestLinkBase):
    # pylint: disable=abstract-method,no-member

    iss = "https://canvas.instructure.com"
    jwt_canvas_keys = {
        "keys": [
            {
                "e": "AQAB",
                "kid": "NtQYzsKs_TWLQ0p3bLmfM7fOwY0nEBVVH3z3Q-zJ06Y",
                "kty": "RSA",
                "n": "uvEnCaUOy1l9gk3wjW3Pib1dBc5g92-6rhvZZOsN1a77fdOqKsrjWG1lDu8kq2nL-wbAzR3DdEPVw"
                "_1WUwtr_Q1d5m-7S4ciXT63pENs1EPwWmeN33O0zkGx8I7vdiOTSVoywEyUZe6UyS-ujLfsRc2Ime"
                "LP5OHxpE1yULEDSiMLtSvgzEaMvf2AkVq5EL5nLYDWXZWXUnpiT_f7iK47Mp2iQd4KYYG7YZ7lMMP"
                "CMBuhej7SOtZQ2FwaBjvZiXDZ172sQYBCiBAmOR3ofTL6aD2-HUxYztVIPCkhyO84mQ7W4BFsOnKW"
                "4WRfEySHXd2hZkFMgcFNXY3dA6de519qlcrL0YYx8ZHpzNt0foEzUsgJd8uJMUVvzPZgExwcyIbv5"
                "jWYBg0ILgULo7ve7VXG5lMwasW_ch2zKp7tTILnDJwITMjF71h4fn4dMTun_7MWEtSl_iFiALnIL_"
                "4_YY717cr4rmcG1424LyxJGRD9L9WjO8etAbPkiRFJUd5fmfqjHkO6fPxyWsMUAu8bfYdVRH7qN_e"
                "rfGHmykmVGgH8AfK9GLT_cjN4GHA29bK9jMed6SWdrkygbQmlnsCAHrw0RA-QE0t617h3uTrSEr5v"
                "kbLz-KThVEBfH84qsweqcac_unKIZ0e2iRuyVnG4cbq8HUdio8gJ62D3wZ0UvVgr4a0",
                "alg": "RS256",
                "use": "sig",
            }
        ]
    }

    post_login_data = {
        "iss": iss,
        "login_hint": "86157096483e6b3a50bfedc6bac902c0b20a824f",
        "target_link_uri": "http://lti.django.test/launch/",
        "lti_message_hint": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2ZXJpZmllciI6Ijg0NjMxZjc1Z"
        "GYxNmNiZjNmYTM5YzEwMzk4YTg0M2U1NTAwZTc5MTU2OTBhN2RjYTJhNGMzMTJjYjR"
        "jOWU0YWY5NzE2MWVhYjg4ODhmOWJlNDc2MmViNzUzZDE5ZmI3YWU5N2I2MjAxZWZjM"
        "jRmODY4NWE3NjJmY2U0ZWU4MDk4IiwiY2FudmFzX2RvbWFpbiI6ImNhbnZhcy5kb2N"
        "rZXIiLCJjb250ZXh0X3R5cGUiOiJDb3Vyc2UiLCJjb250ZXh0X2lkIjoxMDAwMDAwM"
        "DAwMDAwMSwiZXhwIjoxNTY1NDQyMzcwfQ.B1Lddgthaa-YBT4-Lkm3OM_noETl3dIz"
        "5E14YWJ8m_Q",
    }

    post_launch_data = {
        "utf8": "%E2%9C%93",
        "authenticity_token": "oOOlsiqy2nFHP5wgWIKWSEoHKYDZg0u%2BCRKC3BWuFsORmeT2HMC%2BASxQzEoW0"
        "KdnfnZe6ovmOe9gVOqYPth5mw%3D%3D",
        "state": "state-test-uuid-1234",
        "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik50UVl6c0tzX1RXTFEwcDNiTG1mTTdmT3dZMG5FQlZWSDN6M1"
        "EtekowNlkifQ.eyJpc3MiOiJodHRwczovL2NhbnZhcy5pbnN0cnVjdHVyZS5jb20iLCJzdWIiOiJhNmQ1YzQ0My0xZjUxL"
        "TQ3ODMtYmExYS03Njg2ZmZlM2I1NGEiLCJhdWQiOiIxMDAwMDAwMDAwMDAwNCIsImV4cCI6MTU2NTQ0NTY3MCwiaWF0Ijo"
        "xNTY1NDQyMDcwLCJub25jZSI6InRlc3QtdXVpZC0xMjM0IiwibmFtZSI6Ik1zIEphbmUgTWFyaWUgRG9lIiwiZ2l2ZW5fb"
        "mFtZSI6IkphbmUiLCJmYW1pbHlfbmFtZSI6IkRvZSIsImVtYWlsIjoiamFuZUBleGFtcGxlLm9yZyIsImh0dHBzOi8vcHV"
        "ybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL2RlcGxveW1lbnRfaWQiOiI2Ojg4NjVhYTA1YjRiNzliNjRhOTFhO"
        "DYwNDJlNDNhZjVlYThhZTc5ZWIiLCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS9tZXNzYWd"
        "lX3R5cGUiOiJEYXRhUHJpdmFjeUxhdW5jaFJlcXVlc3QiLCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0a"
        "S9jbGFpbS92ZXJzaW9uIjoiMS4zLjAiLCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS9yb2x"
        "lcyI6WyJodHRwOi8vcHVybC5pbXNnbG9iYWwub3JnL3ZvY2FiL2xpcy92Mi9zeXN0ZW0vcGVyc29uI0FkbWluaXN0cmF0b"
        "3IiXSwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGkvY2xhaW0vZm9yX3VzZXIiOnsiaWQiOiI4ZjA0MWQ"
        "5NC05OTQzLTQ2NmItOWRlYi1hNjkyYTZiODVjMDIiLCJwZXJzb25fc291cmNlZGlkIjoiZXhhbXBsZS5lZHU6NzFlZTdlN"
        "DItZjZkMi00MTRhLTgwZGItYjY5YWMyZGVmZDQiLCJnaXZlbl9uYW1lIjoiSnVkZSIsImZhbWlseV9uYW1lIjoiV2lsYmV"
        "ydCIsImVtYWlsIjoiandpbGJlcnRAZXhhbXBsZS5vcmciLCJyb2xlcyI6WyJodHRwOi8vcHVybC5pbXNnbG9iYWwub3JnL"
        "3ZvY2FiL2xpcy92Mi9zeXN0ZW0vcGVyc29uI1VzZXIiXX0sImxvY2FsZSI6ImVuLVVTIiwiaHR0cHM6Ly9wdXJsLmltc2d"
        "sb2JhbC5vcmcvc3BlYy9sdGkvY2xhaW0vdG9vbF9wbGF0Zm9ybSI6eyJuYW1lIjoiRXhhbXBsZSBQbGF0Zm9ybSIsImRlc"
        "2NyaXB0aW9uIjoiUHJvdmlkZXMgYW4gZXhhbXBsZSBvZiBhIHBsYXRmb3JtLiIsImd1aWQiOiIxYjc2M2E4Yy0wZjkxLTQ"
        "2MTUtYmE0Ni1iYzNkNzc2Y2E3ZjgiLCJwcm9kdWN0X2ZhbWlseV9jb2RlIjoiRXhhbXBsZVBsYXRmb3JtIiwidmVyc2lvb"
        "iI6IjEuMC4wLjYiLCJ1cmwiOiJodHRwczovL3BsYXRmb3JtLmV4YW1wbGUub3JnIiwiY29udGFjdF9lbWFpbCI6InNvbWV"
        "vbmVAcGxhdGZvcm0uZXhhbXBsZS5vcmcifSwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGkvY2xhaW0vY"
        "3VzdG9tIjp7IlNvbWVfY3VzdG9tX3NldHRpbmciOiJhX3ZhbHVlMSJ9LCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9"
        "zcGVjL2x0aS9jbGFpbS9saXMiOnsicGVyc29uX3NvdXJjZWRpZCI6ImV4YW1wbGUuZWR1OmI2YjkzMTA1LThkMmYtNGFmO"
        "C05M2VjLTM2YzA1MGI5ODQxMyJ9LCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS9sYXVuY2h"
        "fcHJlc2VudGF0aW9uIjp7InJldHVybl91cmwiOiJodHRwczovL3BsYXRmb3JtLmV4YW1wbGUub3JnL2x0aS9yZXR1cm4if"
        "SwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGkvY2xhaW0vdGFyZ2V0X2xpbmtfdXJpIjoiaHR0cHM6Ly9"
        "wbGF0Zm9ybS5leGFtcGxlLm9yZy9sdGkvcHJpdmFjeSJ9.d3NSZd283wbzzyWLU9i3EHSnNfg1t8J9wDkQXEyPebA9Hnnn"
        "6jsfj0li8BD8_3Q8-sLczLUFEWVDNl6J9U2gtLaGa2gW809Xw9dJ-tQgBgH3bVqRPfcIPVQ_qA5xspXx_lZVp2In4LZUPl"
        "Qh4l81yaIrXauoOsLrtIpqrnsExD1Xva0xtWmCOD-KrTgN4EDWrSj0Tf23siSyjVTRW_ha84zH9WWR4cbXfA2nqzbjE_-5"
        "0pIrzdCI9i5E23q76XEpDO-uxjfWaSo2KdZBkGibQJDPdyWtam1sS5EqbMe0kQBg-5frH-vpaRfkYJ0GWLKULUsaBYYQM-"
        "GG3wVmg4F86Oxvwb0fGOO6lGQx9arqoUlkCPCAmvmg7wuK7dBF7a2KZBwa1LYxtAFetQbdQs5FhLKFiQFw7IxbDza4A1aP"
        "N-DHwMZxFQT4nfewuC-bhU4TmYkbxO3csDYtk5ng97EY3JxaFIXYqUj9w0W8y7Dj_1qmQIVIc_pQU594YZCSbl06DWGCD1"
        "uKyJu0PRj6Sa3T3hG6ecqvQaf6V_OwgEd-u_f6qXbmUYstb9l8sW3yWcB6PH7-OC-I9Ttoy4vSKkPQRZ-9Tu2LZlXjMnRF"
        "odIoYA-LekMYldb0sabYT4yw1pmXAo5dyMfGSHIjJ21-xAiaqFTpfQ5b3fgmIlv-oZYda1c",
    }

    expected_message_launch_data = {
        "iss": "https://canvas.instructure.com",
        "sub": "a6d5c443-1f51-4783-ba1a-7686ffe3b54a",
        "aud": "10000000000004",
        "exp": 1565445670,
        "iat": 1565442070,
        "nonce": "test-uuid-1234",
        "name": "Ms Jane Marie Doe",
        "given_name": "Jane",
        "family_name": "Doe",
        "email": "jane@example.org",
        "https://purl.imsglobal.org/spec/lti/claim/deployment_id": "6:8865aa05b4b79b64a91a86042e43af5ea8ae79eb",
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
            "roles": ["http://purl.imsglobal.org/vocab/lis/v2/system/person#User"],
        },
        "locale": "en-US",
        "https://purl.imsglobal.org/spec/lti/claim/tool_platform": {
            "name": "Example Platform",
            "description": "Provides an example of a platform.",
            "guid": "1b763a8c-0f91-4615-ba46-bc3d776ca7f8",
            "product_family_code": "ExamplePlatform",
            "version": "1.0.0.6",
            "url": "https://platform.example.org",
            "contact_email": "someone@platform.example.org",
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
        "https://purl.imsglobal.org/spec/lti/claim/target_link_uri": "https://platform.example.org/lti/privacy",
    }

    def test_privacy_launch_success(self):
        tool_conf, login_request, login_response = self._make_oidc_login()
        launch_request = self._get_request(login_request, login_response)
        validated_message_launch = self._launch(
            launch_request, tool_conf, force_validation=True
        )
        message_launch_data = validated_message_launch.get_launch_data()
        self.assertDictEqual(message_launch_data, self.expected_message_launch_data)
        self.assertTrue(validated_message_launch.is_data_privacy_launch())
        self.assertDictEqual(
            validated_message_launch.get_data_privacy_launch_user(),
            self.expected_message_launch_data.get(
                "https://purl.imsglobal.org/spec/lti/claim/for_user"
            ),
        )


class TestDjangoPrivacyLaunch(DjangoMixin, PrivacyLaunchBase):
    pass


class TestFlaskPrivacyLaunch(FlaskMixin, PrivacyLaunchBase):
    pass
