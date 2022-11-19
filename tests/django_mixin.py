from unittest.mock import patch
from urllib.parse import quote
from .request import FakeRequest
from .response import FakeResponse
from .tool_config import get_test_tool_conf, TOOL_CONFIG


class DjangoMixin:
    # pylint: disable=import-outside-toplevel

    def _get_request(
        self,
        login_request,
        login_response,
        request_is_secure=False,
        post_data=None,
        empty_session=False,
        empty_cookies=False,
    ):
        session = None if empty_session else login_request.session
        cookies = None if empty_cookies else login_response.get_cookies_dict()
        post_launch_data = post_data if post_data else self.post_launch_data
        return FakeRequest(
            post=post_launch_data,
            cookies=cookies,
            session=session,
            secure=request_is_secure,
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
        request = None
        login_data = {}
        if not uuid_val:
            uuid_val = "test-uuid-1234"

        if self.get_login_data:
            request = FakeRequest(get=self.get_login_data, secure=secure)
            login_data = self.get_login_data.copy()
        elif self.post_login_data:
            request = FakeRequest(post=self.post_login_data, secure=secure)
            login_data = self.post_login_data.copy()

        with patch("django.shortcuts.redirect") as mock_redirect:
            from pylti1p3.contrib.django import DjangoOIDCLogin

            with patch.object(
                DjangoOIDCLogin, "_get_uuid", autospec=True
            ) as get_uuid, patch.object(
                DjangoOIDCLogin, "_generate_nonce", autospec=True
            ) as generate_nonce, patch.object(
                DjangoOIDCLogin, "get_response", autospec=True
            ) as get_response:
                get_uuid.side_effect = (
                    lambda x: uuid_val
                )  # pylint: disable=unnecessary-lambda
                generate_nonce.side_effect = (
                    lambda x: uuid_val
                )  # pylint: disable=unnecessary-lambda
                get_response.side_effect = lambda y, html: html
                oidc_login = DjangoOIDCLogin(request, tool_conf)

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
                    request = FakeRequest(get=login_data, secure=secure)

                    oidc_login = DjangoOIDCLogin(request, tool_conf)
                    oidc_login.enable_check_cookies()

                response = oidc_login.redirect(launch_url)

                # check cookie data
                self.assertEqual(len(response.cookies), 1)
                self.assertTrue(("lti1p3-state-" + uuid_val) in response.cookies)
                self.assertEqual(
                    response.cookies["lti1p3-state-" + uuid_val]["value"],
                    "state-" + uuid_val,
                )

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
                redirect_url = response.data  # pylint: disable=no-member
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
                self.assertTrue(len(response.cookies), 1)
                cookie_key = list(response.cookies)[0]
                cookie_dict = response.cookies[cookie_key]
                if secure:
                    self.assertTrue(cookie_dict["secure"])
                    self.assertEqual(cookie_dict["samesite"], "None")
                else:
                    self.assertFalse(cookie_dict["secure"])
                    self.assertTrue("samesite" not in cookie_dict)

        return tool_conf, request, response

    def _get_launch_obj(self, request, tool_conf, cache=False):
        from pylti1p3.contrib.django import DjangoMessageLaunch

        message_launch = DjangoMessageLaunch(request, tool_conf)
        if cache:
            message_launch.set_launch_data_storage(cache)
        return message_launch

    def _get_launch_cls(self):
        from pylti1p3.contrib.django import DjangoMessageLaunch

        return DjangoMessageLaunch
