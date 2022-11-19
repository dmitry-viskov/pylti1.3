from parameterized import parameterized
from pylti1p3.exception import LtiException
from .base import TestLinkBase
from .cache import FakeCacheDataStorage
from .django_mixin import DjangoMixin
from .flask_mixin import FlaskMixin


class ResourceLinkBase(TestLinkBase):
    # pylint: disable=abstract-method,no-member

    iss = "https://canvas.instructure.com"
    jwt_canvas_keys = {
        "keys": [
            {
                "kty": "RSA",
                "e": "AQAB",
                "n": "uX1MpfEMQCBUMcj0sBYI-iFaG5Nodp3C6OlN8uY60fa5zSBd83-iIL3n_qzZ8VCluuTLfB7rrV_tiX727XIEqQ",
                "kid": "2018-05-18T22:33:20Z",
            },
            {
                "kty": "RSA",
                "e": "AQAB",
                "n": "uX1MpfEMQCBUMcj0sBYI-iFaG5Nodp3C6OlN8uY60fa5zSBd83-iIL3n_qzZ8VCluuTLfB7rrV_tiX727XIEqQ",
                "kid": "2018-06-18T22:33:20Z",
            },
            {
                "kty": "RSA",
                "e": "AQAB",
                "n": "uX1MpfEMQCBUMcj0sBYI-iFaG5Nodp3C6OlN8uY60fa5zSBd83-iIL3n_qzZ8VCluuTLfB7rrV_tiX727XIEqQ",
                "kid": "2018-07-18T22:33:20Z",
            },
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
        "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTgtMDYtMThUMjI6MzM6MjBaIn0."
        "eyJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS9tZXNzYWdlX3R5cGUi"
        "OiJMdGlSZXNvdXJjZUxpbmtSZXF1ZXN0IiwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3Bl"
        "Yy9sdGkvY2xhaW0vdmVyc2lvbiI6IjEuMy4wIiwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcv"
        "c3BlYy9sdGkvY2xhaW0vcmVzb3VyY2VfbGluayI6eyJpZCI6IjRkZGUwNWU4Y2ExOTczYmNjYTli"
        "ZmZjMTNlMTU0ODgyMGVlZTkzYTMiLCJkZXNjcmlwdGlvbiI6bnVsbCwidGl0bGUiOm51bGwsInZh"
        "bGlkYXRpb25fY29udGV4dCI6bnVsbCwiZXJyb3JzIjp7ImVycm9ycyI6e319fSwiYXVkIjoiMTAw"
        "MDAwMDAwMDAwMDQiLCJhenAiOiIxMDAwMDAwMDAwMDAwNCIsImh0dHBzOi8vcHVybC5pbXNnbG9i"
        "YWwub3JnL3NwZWMvbHRpL2NsYWltL2RlcGxveW1lbnRfaWQiOiI2Ojg4NjVhYTA1YjRiNzliNjRh"
        "OTFhODYwNDJlNDNhZjVlYThhZTc5ZWIiLCJleHAiOjE1NjU0NDU2NzAsImlhdCI6MTU2NTQ0MjA3"
        "MCwiaXNzIjoiaHR0cHM6Ly9jYW52YXMuaW5zdHJ1Y3R1cmUuY29tIiwibm9uY2UiOiJ0ZXN0LXV1"
        "aWQtMTIzNCIsInN1YiI6ImE0NDVjYTk5LTFhNjQtNDY5Ny05YmZhLTUwOGExMTgyNDVlYSIsImh0"
        "dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL3RhcmdldF9saW5rX3VyaSI6"
        "Imh0dHA6Ly9sdGkuZGphbmdvLnRlc3QvbGF1bmNoLyIsImh0dHBzOi8vcHVybC5pbXNnbG9iYWwu"
        "b3JnL3NwZWMvbHRpL2NsYWltL2NvbnRleHQiOnsiaWQiOiI0ZGRlMDVlOGNhMTk3M2JjY2E5YmZm"
        "YzEzZTE1NDg4MjBlZWU5M2EzIiwibGFiZWwiOiJUZXN0IiwidGl0bGUiOiJUZXN0IiwidHlwZSI6"
        "WyJodHRwOi8vcHVybC5pbXNnbG9iYWwub3JnL3ZvY2FiL2xpcy92Mi9jb3Vyc2UjQ291cnNlT2Zm"
        "ZXJpbmciXSwidmFsaWRhdGlvbl9jb250ZXh0IjpudWxsLCJlcnJvcnMiOnsiZXJyb3JzIjp7fX19"
        "LCJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS9jbGFpbS90b29sX3BsYXRmb3Jt"
        "Ijp7Imd1aWQiOiJDZUFEeks3aHNQWWZ6bXlDN0xUTDhjcHpaSVNOZHBXalZnMVVaakxZOmNhbnZh"
        "cy1sbXMiLCJuYW1lIjoiRG1pdHJ5T3JnIiwidmVyc2lvbiI6ImNsb3VkIiwicHJvZHVjdF9mYW1p"
        "bHlfY29kZSI6ImNhbnZhcyIsInZhbGlkYXRpb25fY29udGV4dCI6bnVsbCwiZXJyb3JzIjp7ImVy"
        "cm9ycyI6e319fSwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGkvY2xhaW0vbGF1"
        "bmNoX3ByZXNlbnRhdGlvbiI6eyJkb2N1bWVudF90YXJnZXQiOiJpZnJhbWUiLCJoZWlnaHQiOm51"
        "bGwsIndpZHRoIjpudWxsLCJyZXR1cm5fdXJsIjoiaHR0cDovL2NhbnZhcy5kb2NrZXIvY291cnNl"
        "cy8xL2V4dGVybmFsX2NvbnRlbnQvc3VjY2Vzcy9leHRlcm5hbF90b29sX3JlZGlyZWN0IiwibG9j"
        "YWxlIjoiZW4iLCJ2YWxpZGF0aW9uX2NvbnRleHQiOm51bGwsImVycm9ycyI6eyJlcnJvcnMiOnt9"
        "fX0sImxvY2FsZSI6ImVuIiwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGkvY2xh"
        "aW0vcm9sZXMiOlsiaHR0cDovL3B1cmwuaW1zZ2xvYmFsLm9yZy92b2NhYi9saXMvdjIvaW5zdGl0"
        "dXRpb24vcGVyc29uI0FkbWluaXN0cmF0b3IiLCJodHRwOi8vcHVybC5pbXNnbG9iYWwub3JnL3Zv"
        "Y2FiL2xpcy92Mi9zeXN0ZW0vcGVyc29uI1N5c0FkbWluIiwiaHR0cDovL3B1cmwuaW1zZ2xvYmFs"
        "Lm9yZy92b2NhYi9saXMvdjIvc3lzdGVtL3BlcnNvbiNVc2VyIl0sImh0dHBzOi8vcHVybC5pbXNn"
        "bG9iYWwub3JnL3NwZWMvbHRpL2NsYWltL2N1c3RvbSI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNv"
        "bSIsInVzZXJfaWQiOjJ9LCJlcnJvcnMiOnsiZXJyb3JzIjp7fX0sImh0dHBzOi8vcHVybC5pbXNn"
        "bG9iYWwub3JnL3NwZWMvbHRpLWFncy9jbGFpbS9lbmRwb2ludCI6eyJzY29wZSI6WyJodHRwczov"
        "L3B1cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS1hZ3Mvc2NvcGUvc2NvcmUiLCJodHRwczovL3B1"
        "cmwuaW1zZ2xvYmFsLm9yZy9zcGVjL2x0aS1hZ3Mvc2NvcGUvcmVzdWx0LnJlYWRvbmx5IiwiaHR0"
        "cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGktYWdzL3Njb3BlL2xpbmVpdGVtLnJlYWRv"
        "bmx5IiwiaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGktYWdzL3Njb3BlL2xpbmVp"
        "dGVtIl0sImxpbmVpdGVtcyI6Imh0dHA6Ly9jYW52YXMuZG9ja2VyL2FwaS9sdGkvY291cnNlcy8x"
        "L2xpbmVfaXRlbXMiLCJ2YWxpZGF0aW9uX2NvbnRleHQiOm51bGwsImVycm9ycyI6eyJlcnJvcnMi"
        "Ont9fX0sImh0dHBzOi8vcHVybC5pbXNnbG9iYWwub3JnL3NwZWMvbHRpLW5ycHMvY2xhaW0vbmFt"
        "ZXNyb2xlc2VydmljZSI6eyJjb250ZXh0X21lbWJlcnNoaXBzX3VybCI6Imh0dHA6Ly9jYW52YXMu"
        "ZG9ja2VyL2FwaS9sdGkvY291cnNlcy8xL25hbWVzX2FuZF9yb2xlcyIsInNlcnZpY2VfdmVyc2lv"
        "bnMiOlsiMi4wIl0sInZhbGlkYXRpb25fY29udGV4dCI6bnVsbCwiZXJyb3JzIjp7ImVycm9ycyI6"
        "e319fX0.XR7ED7t3GVksBKO12gh99dvTgEhWtwcEgmJUqrdeU9UYGKyU7AX8r3hpmsonyItZnTOH"
        "wuITv7Y0ejn033RypQ",
    }

    expected_message_launch_data = {
        "nonce": "test-uuid-1234",
        "https://purl.imsglobal.org/spec/lti/claim/tool_platform": {
            "errors": {"errors": {}},
            "name": "DmitryOrg",
            "version": "cloud",
            "product_family_code": "canvas",
            "guid": "CeADzK7hsPYfzmyC7LTL8cpzZISNdpWjVg1UZjLY:canvas-lms",
            "validation_context": None,
        },
        "https://purl.imsglobal.org/spec/lti/claim/context": {
            "errors": {"errors": {}},
            "title": "Test",
            "label": "Test",
            "type": ["http://purl.imsglobal.org/vocab/lis/v2/course#CourseOffering"],
            "id": "4dde05e8ca1973bcca9bffc13e1548820eee93a3",
            "validation_context": None,
        },
        "errors": {"errors": {}},
        "aud": "10000000000004",
        "https://purl.imsglobal.org/spec/lti/claim/version": "1.3.0",
        "iss": "https://canvas.instructure.com",
        "https://purl.imsglobal.org/spec/lti/claim/roles": [
            "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Administrator",
            "http://purl.imsglobal.org/vocab/lis/v2/system/person#SysAdmin",
            "http://purl.imsglobal.org/vocab/lis/v2/system/person#User",
        ],
        "https://purl.imsglobal.org/spec/lti/claim/custom": {
            "user_id": 2,
            "email": "admin@admin.com",
        },
        "https://purl.imsglobal.org/spec/lti-nrps/claim/namesroleservice": {
            "context_memberships_url": "http://canvas.docker/api/lti/courses/1/names_and_roles",
            "service_versions": ["2.0"],
            "errors": {"errors": {}},
            "validation_context": None,
        },
        "locale": "en",
        "https://purl.imsglobal.org/spec/lti/claim/resource_link": {
            "errors": {"errors": {}},
            "validation_context": None,
            "title": None,
            "id": "4dde05e8ca1973bcca9bffc13e1548820eee93a3",
            "description": None,
        },
        "https://purl.imsglobal.org/spec/lti/claim/message_type": "LtiResourceLinkRequest",
        "https://purl.imsglobal.org/spec/lti/claim/deployment_id": "6:8865aa05b4b79b64a91a86042e43af5ea8ae79eb",
        "iat": 1565442070,
        "azp": "10000000000004",
        "exp": 1565445670,
        "https://purl.imsglobal.org/spec/lti-ags/claim/endpoint": {
            "scope": [
                "https://purl.imsglobal.org/spec/lti-ags/scope/score",
                "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly",
                "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly",
                "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
            ],
            "lineitems": "http://canvas.docker/api/lti/courses/1/line_items",
            "errors": {"errors": {}},
            "validation_context": None,
        },
        "https://purl.imsglobal.org/spec/lti/claim/launch_presentation": {
            "errors": {"errors": {}},
            "locale": "en",
            "height": None,
            "width": None,
            "document_target": "iframe",
            "return_url": "http://canvas.docker/courses/1/external_content/success/external_tool_redirect",
            "validation_context": None,
        },
        "https://purl.imsglobal.org/spec/lti/claim/target_link_uri": "http://lti.django.test/launch/",
        "sub": "a445ca99-1a64-4697-9bfa-508a118245ea",
    }

    def _launch_success(
        self,
        tool_conf_cls=None,
        secure=False,
        tool_conf_extended=False,
        enable_check_cookies=False,
        use_cache=False,
    ):
        cache = FakeCacheDataStorage() if use_cache else False
        tool_conf, login_request, login_response = self._make_oidc_login(
            tool_conf_cls=tool_conf_cls,
            secure=secure,
            tool_conf_extended=tool_conf_extended,
            enable_check_cookies=enable_check_cookies,
            cache=cache,
        )
        launch_request = self._get_request(
            login_request, login_response, request_is_secure=secure
        )
        message_launch_data = self._launch(launch_request, tool_conf, cache=cache)
        self.assertDictEqual(message_launch_data, self.expected_message_launch_data)

    @parameterized.expand(
        [
            ["base_non_secure", False, False],
            ["base_secure", True, False],
            ["tool_conf_one_iss_many_clients", False, True],
        ]
    )
    def test_res_link_launch_success(
        self, name, secure, tool_conf_extended  # pylint: disable=unused-argument
    ):
        self._launch_success(None, secure, tool_conf_extended)

    def test_res_link_check_cookies_page(self):
        self._launch_success(enable_check_cookies=True)

    def test_res_link_check_launch_data_storage(self):
        self._launch_success(use_cache=True)

    def test_res_link_launch_invalid_public_key(self):
        tool_conf, login_request, login_response = self._make_oidc_login()

        launch_request = self._get_request(login_request, login_response)
        with self.assertRaisesRegex(LtiException, "Invalid response"):
            self._launch(launch_request, tool_conf, "invalid_key_set")

    def test_res_link_launch_invalid_state(self):
        tool_conf, login_request, login_response = self._make_oidc_login()

        post_data = self.post_launch_data.copy()
        post_data.pop("state", None)

        launch_request = self._get_request(
            login_request, login_response, post_data=post_data
        )
        with self.assertRaisesRegex(LtiException, "Missing state param"):
            self._launch(launch_request, tool_conf)

        launch_request = self._get_request(
            login_request, login_response, empty_cookies=True
        )
        with self.assertRaisesRegex(LtiException, "State not found"):
            self._launch(launch_request, tool_conf)

    def test_res_link_launch_invalid_jwt_format(self):
        tool_conf, login_request, login_response = self._make_oidc_login()

        post_data = self.post_launch_data.copy()
        post_data["id_token"] += ".absjdbasdj"

        launch_request = self._get_request(
            login_request, login_response, post_data=post_data
        )
        with self.assertRaisesRegex(LtiException, "Invalid id_token"):
            self._launch(launch_request, tool_conf)

        post_data = self.post_launch_data.copy()
        post_data["id_token"] = "jbafjjsdbjasdabsjdbasdj1212121212.sdfhdhsf.sdfdsfdsf"

        launch_request = self._get_request(
            login_request, login_response, post_data=post_data
        )
        with self.assertRaisesRegex(LtiException, "Invalid JWT format"):
            self._launch(launch_request, tool_conf)

    def test_res_link_launch_invalid_jwt_signature(self):
        tool_conf, login_request, login_response = self._make_oidc_login()

        post_data = self.post_launch_data.copy()
        post_data["id_token"] += "jbafjjsdbjasdabsjdbasdj"

        launch_request = self._get_request(
            login_request, login_response, post_data=post_data
        )
        with self.assertRaisesRegex(LtiException, "Can't decode id_token"):
            self._launch(launch_request, tool_conf)

    def _get_data_without_nonce(self, *args):  # pylint: disable=unused-argument
        message_launch_data = self.expected_message_launch_data.copy()
        message_launch_data.pop("nonce", None)
        return message_launch_data

    def _get_data_with_invalid_aud(self, *args):  # pylint: disable=unused-argument
        message_launch_data = self.expected_message_launch_data.copy()
        message_launch_data["aud"] = "dsfsdfsdfsdfsd"
        return message_launch_data

    def _get_data_with_invalid_deployment(
        self, *args
    ):  # pylint: disable=unused-argument
        message_launch_data = self.expected_message_launch_data.copy()
        message_launch_data[
            "https://purl.imsglobal.org/spec/lti/claim/deployment_id"
        ] = "dsfsdfsdfsdfsd"
        return message_launch_data

    def _get_data_with_invalid_message(self, *args):  # pylint: disable=unused-argument
        message_launch_data = self.expected_message_launch_data.copy()
        message_launch_data[
            "https://purl.imsglobal.org/spec/lti/claim/version"
        ] = "1.2.0"
        return message_launch_data

    def test_res_link_launch_invalid_nonce(self):

        tool_conf, login_request, login_response = self._make_oidc_login()

        post_data = self.post_launch_data.copy()
        launch_request = self._get_request(
            login_request, login_response, post_data=post_data
        )

        with self.assertRaisesRegex(LtiException, '"nonce" is empty'):
            self._launch_with_invalid_jwt_body(
                self._get_data_without_nonce, launch_request, tool_conf
            )

        launch_request = self._get_request(
            login_request, login_response, post_data=post_data, empty_session=True
        )

        with self.assertRaisesRegex(LtiException, "Invalid Nonce"):
            self._launch(launch_request, tool_conf)

    def test_res_link_launch_invalid_registration(self):
        tool_conf, login_request, login_response = self._make_oidc_login()

        post_data = self.post_launch_data.copy()
        launch_request = self._get_request(
            login_request, login_response, post_data=post_data
        )

        with self.assertRaisesRegex(
            LtiException, "Client id not registered for this issuer"
        ):
            self._launch_with_invalid_jwt_body(
                self._get_data_with_invalid_aud, launch_request, tool_conf
            )

    def test_res_link_launch_invalid_deployment(self):
        tool_conf, login_request, login_response = self._make_oidc_login()

        post_data = self.post_launch_data.copy()
        launch_request = self._get_request(
            login_request, login_response, post_data=post_data
        )

        with self.assertRaisesRegex(Exception, "Unable to find deployment"):
            self._launch_with_invalid_jwt_body(
                self._get_data_with_invalid_deployment, launch_request, tool_conf
            )

    def test_res_link_launch_invalid_message(self):
        tool_conf, login_request, login_response = self._make_oidc_login()

        post_data = self.post_launch_data.copy()
        launch_request = self._get_request(
            login_request, login_response, post_data=post_data
        )

        with self.assertRaisesRegex(LtiException, "Incorrect version"):
            self._launch_with_invalid_jwt_body(
                self._get_data_with_invalid_message, launch_request, tool_conf
            )


class TestDjangoResourceLink(DjangoMixin, ResourceLinkBase):
    pass


class TestFlaskResourceLink(FlaskMixin, ResourceLinkBase):
    pass
