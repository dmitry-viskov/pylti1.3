from unittest.mock import patch
from urllib.parse import quote
from pylti1p3.contrib.flask import FlaskRequest, FlaskCookieService, FlaskSessionService
from .response import FakeResponse
from .tool_config import get_test_tool_conf, TOOL_CONFIG


class FlaskMixin:
    # pylint: disable=import-outside-toplevel

    def get_cookies_dict_from_response(self, response):
        cookie_name, cookie_value = (
            response.headers["Set-Cookie"].split(";")[0].split("=")
        )
        return {cookie_name: cookie_value}

    def _get_request(
        self,
        login_request,
        login_response,
        request_is_secure=False,
        post_data=None,
        empty_session=False,
        empty_cookies=False,
    ):
        session = {} if empty_session else login_request.session
        cookies = (
            {} if empty_cookies else self.get_cookies_dict_from_response(login_response)
        )
        post_launch_data = post_data if post_data else self.post_launch_data
        return FlaskRequest(
            request_data=post_launch_data,
            cookies=cookies,
            session=session,
            request_is_secure=request_is_secure,
        )

    def _make_oidc_login(
        self,
        uuid_val=None,
        tool_conf_cls=None,
        secure=False,
        tool_conf_extended=False,
        enable_check_cookies=False,
        cache=False,
    ):
        # pylint: disable=too-many-statements
        tool_conf = get_test_tool_conf(tool_conf_cls, tool_conf_extended)
        if not uuid_val:
            uuid_val = "test-uuid-1234"

        login_data = {
            "iss": "https://canvas.instructure.com",
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

        request = FlaskRequest(
            request_data=login_data, cookies={}, session={}, request_is_secure=secure
        )

        with patch("flask.redirect") as mock_redirect:
            from pylti1p3.contrib.flask import FlaskOIDCLogin

            with patch.object(
                FlaskOIDCLogin, "_get_uuid", autospec=True
            ) as get_uuid, patch.object(
                FlaskOIDCLogin, "_generate_nonce", autospec=True
            ) as generate_nonce, patch.object(
                FlaskOIDCLogin, "get_response", autospec=True
            ) as get_response:
                get_uuid.side_effect = (
                    lambda x: uuid_val
                )  # pylint: disable=unnecessary-lambda
                generate_nonce.side_effect = (
                    lambda x: uuid_val
                )  # pylint: disable=unnecessary-lambda
                get_response.side_effect = lambda y, html: html

                oidc_login = FlaskOIDCLogin(
                    request,
                    tool_conf,
                    cookie_service=FlaskCookieService(request),
                    session_service=FlaskSessionService(request),
                )

                if cache:
                    oidc_login.set_launch_data_storage(cache)

                # pylint: disable=unnecessary-lambda
                mock_redirect.side_effect = lambda x: FakeResponse(x)
                launch_url = "http://lti.django.test/launch/"

                if enable_check_cookies:
                    response_html = oidc_login.enable_check_cookies().redirect(
                        launch_url
                    )
                    self.assertTrue('<script type="text/javascript">' in response_html)
                    self.assertTrue("<body>" in response_html)
                    self.assertTrue(
                        'document.addEventListener("DOMContentLoaded", checkCookiesAllowed);'
                        in response_html
                    )

                    login_data["lti1p3_new_window"] = "1"
                    request = FlaskRequest(
                        request_data=login_data,
                        cookies={},
                        session={},
                        request_is_secure=secure,
                    )

                    oidc_login = FlaskOIDCLogin(
                        request,
                        tool_conf,
                        cookie_service=FlaskCookieService(request),
                        session_service=FlaskSessionService(request),
                    )
                    oidc_login.enable_check_cookies()

                response = oidc_login.redirect(launch_url)

                # check cookie data
                self.assertTrue("Set-Cookie" in response.headers)
                set_cookie_header = response.headers["Set-Cookie"]
                expected_cookie = "lti1p3-state-" + uuid_val + "=state-" + uuid_val
                self.assertTrue(expected_cookie in set_cookie_header)

                if secure:
                    self.assertTrue("Secure" in set_cookie_header)
                    self.assertTrue("SameSite=None" in set_cookie_header)
                else:
                    self.assertFalse("Secure" in set_cookie_header)
                    self.assertFalse("SameSite" in set_cookie_header)

                # check session data
                if cache:
                    # pylint: disable=protected-access
                    self.assertEqual(
                        len(oidc_login._session_service.data_storage._cache._data), 1
                    )
                else:
                    self.assertEqual(len(request.session), 1)
                    self.assertEqual(request.session["lti1p3-nonce-" + uuid_val], True)

                # check redirect_url
                redirect_url = response.location
                self.assertTrue(
                    redirect_url.startswith(
                        TOOL_CONFIG[login_data["iss"]]["auth_login_url"]
                    )
                )
                url_params = redirect_url.split("?")[1].split("&")
                self.assertTrue(("nonce=" + uuid_val) in url_params)
                self.assertTrue(("state=state-" + uuid_val) in url_params)
                self.assertTrue(("state=state-" + uuid_val) in url_params)
                self.assertTrue("prompt=none" in url_params)
                self.assertTrue("response_type=id_token" in url_params)
                self.assertTrue(
                    ("client_id=" + TOOL_CONFIG[login_data["iss"]]["client_id"])
                    in url_params
                )
                self.assertTrue(
                    ("login_hint=" + login_data["login_hint"]) in url_params
                )
                self.assertTrue(
                    ("lti_message_hint=" + login_data["lti_message_hint"]) in url_params
                )
                self.assertTrue("scope=openid" in url_params)
                self.assertTrue("response_mode=form_post" in url_params)
                self.assertTrue(("redirect_uri=" + quote(launch_url, "")) in url_params)

        return tool_conf, request, response

    def _get_launch_obj(self, request, tool_conf, cache=False):
        from pylti1p3.contrib.flask import FlaskMessageLaunch

        message_launch = FlaskMessageLaunch(
            request,
            tool_conf,
            cookie_service=FlaskCookieService(request),
            session_service=FlaskSessionService(request),
        )
        if cache:
            message_launch.set_launch_data_storage(cache)
        return message_launch

    def _get_launch_cls(self):
        from pylti1p3.contrib.flask import FlaskMessageLaunch

        return FlaskMessageLaunch
