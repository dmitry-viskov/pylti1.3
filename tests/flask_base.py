import json
import unittest
import requests_mock

from pylti1p3.contrib.flask import FlaskRequest, FlaskCookieService, \
    FlaskSessionService

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
from .response import FakeResponse
from .tool_config import get_test_tool_conf, TOOL_CONFIG


class TestFlaskLinkBase(unittest.TestCase):
    iss = 'replace-me'

    def _make_oidc_login(self, secure, uuid_val=None, tool_conf_cls=None):
        tool_conf = get_test_tool_conf(tool_conf_cls)
        if not uuid_val:
            uuid_val = 'test-uuid-1234'

        login_data = {
            'iss': 'https://canvas.instructure.com',
            'login_hint': '86157096483e6b3a50bfedc6bac902c0b20a824f',
            'target_link_uri': 'http://lti.django.test/launch/',
            'lti_message_hint': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2ZXJpZmllciI6Ijg0NjMxZjc1Z'
                                'GYxNmNiZjNmYTM5YzEwMzk4YTg0M2U1NTAwZTc5MTU2OTBhN2RjYTJhNGMzMTJjYjR'
                                'jOWU0YWY5NzE2MWVhYjg4ODhmOWJlNDc2MmViNzUzZDE5ZmI3YWU5N2I2MjAxZWZjM'
                                'jRmODY4NWE3NjJmY2U0ZWU4MDk4IiwiY2FudmFzX2RvbWFpbiI6ImNhbnZhcy5kb2N'
                                'rZXIiLCJjb250ZXh0X3R5cGUiOiJDb3Vyc2UiLCJjb250ZXh0X2lkIjoxMDAwMDAwM'
                                'DAwMDAwMSwiZXhwIjoxNTY1NDQyMzcwfQ.B1Lddgthaa-YBT4-Lkm3OM_noETl3dIz'
                                '5E14YWJ8m_Q'
        }

        request = FlaskRequest(
            request_kwargs=login_data,
            cookies={},
            session={},
            is_secure=secure
        )

        with patch('flask.redirect') as mock_redirect:
            from pylti1p3.contrib.flask import FlaskOIDCLogin
            with patch.object(FlaskOIDCLogin, "_get_uuid", autospec=True) as get_uuid:
                get_uuid.side_effect = lambda x: uuid_val  # pylint: disable=unnecessary-lambda
                oidc_login = FlaskOIDCLogin(request, tool_conf,
                                            cookie_service=FlaskCookieService(request),
                                            session_service=FlaskSessionService(request))
                mock_redirect.side_effect = lambda x: FakeResponse(x)  # pylint: disable=unnecessary-lambda
                launch_url = 'http://lti.django.test/launch/'
                response = oidc_login.redirect(launch_url)

                # check cookie data
                self.assertTrue('Set-Cookie' in response.headers)
                set_cookie_header = response.headers['Set-Cookie']
                expected_cookie = 'lti1p3-state-' + uuid_val + '=state-' + uuid_val
                self.assertTrue(expected_cookie in set_cookie_header)

                if secure:
                    self.assertTrue('Secure' in set_cookie_header)
                else:
                    self.assertFalse('Secure' in set_cookie_header)

                # check session data
                self.assertEqual(len(request.session), 1)
                self.assertEqual(request.session['lti1p3-nonce-' + uuid_val], True)

                # check redirect_url
                redirect_url = response.location
                self.assertTrue(redirect_url.startswith(TOOL_CONFIG[login_data['iss']]['auth_login_url']))
                url_params = redirect_url.split('?')[1].split('&')
                self.assertTrue(('nonce=' + uuid_val) in url_params)
                self.assertTrue(('state=state-' + uuid_val) in url_params)
                self.assertTrue(('state=state-' + uuid_val) in url_params)
                self.assertTrue('prompt=none' in url_params)
                self.assertTrue('response_type=id_token' in url_params)
                self.assertTrue(('client_id=' + TOOL_CONFIG[login_data['iss']]['client_id']) in url_params)
                self.assertTrue(('login_hint=' + login_data['login_hint']) in url_params)
                self.assertTrue(('lti_message_hint=' + login_data['lti_message_hint']) in url_params)
                self.assertTrue('scope=openid' in url_params)
                self.assertTrue('response_mode=form_post' in url_params)
                self.assertTrue(('redirect_uri=' + quote(launch_url, '')) in url_params)

        return tool_conf, request, response

    def _launch(self, request, tool_conf, key_set_url_response=None, force_validation=False):
        from pylti1p3.contrib.flask import FlaskMessageLaunch
        obj = FlaskMessageLaunch(request, tool_conf,
                                 cookie_service=FlaskCookieService(request),
                                 session_service=FlaskSessionService(request))
        obj.set_jwt_verify_options({
            'verify_aud': False,
            'verify_exp': False
        })

        with patch('socket.gethostbyname', return_value="127.0.0.1"):
            with requests_mock.Mocker() as m:
                key_set_url_text = key_set_url_response if key_set_url_response else json.dumps(self.jwt_canvas_keys)
                m.get(TOOL_CONFIG[self.iss]['key_set_url'], text=key_set_url_text)
                if force_validation:
                    return obj.validate()
                else:
                    return obj.get_launch_data()

    def _launch_with_invalid_jwt_body(self, side_effect, request, tool_conf):
        from pylti1p3.contrib.flask import FlaskMessageLaunch
        with patch.object(FlaskMessageLaunch, "_get_jwt_body", autospec=True) as get_jwt_body:
            get_jwt_body.side_effect = side_effect
            return self._launch(request, tool_conf, force_validation=True)
