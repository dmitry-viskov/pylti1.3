try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
from .request import FakeRequest
from .response import FakeResponse
from .tool_config import get_test_tool_conf, TOOL_CONFIG


class DjangoMixin(object):

    def _get_django_request(self, login_request, login_response, post_data=None,
                            empty_session=False, empty_cookies=False):
        session = None if empty_session else login_request.session
        cookies = None if empty_cookies else login_response.get_cookies_dict()
        post_launch_data = post_data if post_data else self.post_launch_data
        return FakeRequest(post=post_launch_data,
                           cookies=cookies,
                           session=session)

    def _make_django_oidc_login(self, uuid_val=None, tool_conf_cls=None):
        tool_conf = get_test_tool_conf(tool_conf_cls)
        request = None
        login_data = {}
        if not uuid_val:
            uuid_val = 'test-uuid-1234'

        if self.get_login_data:
            request = FakeRequest(get=self.get_login_data)
            login_data = self.get_login_data.copy()
        elif self.post_login_data:
            request = FakeRequest(post=self.post_login_data)
            login_data = self.post_login_data.copy()

        with patch('django.shortcuts.redirect') as mock_redirect:
            from pylti1p3.contrib.django import DjangoOIDCLogin
            with patch.object(DjangoOIDCLogin, "_get_uuid", autospec=True) as get_uuid:
                get_uuid.side_effect = lambda x: uuid_val  # pylint: disable=unnecessary-lambda
                oidc_login = DjangoOIDCLogin(request, tool_conf)
                mock_redirect.side_effect = lambda x: FakeResponse(x)  # pylint: disable=unnecessary-lambda
                launch_url = 'http://lti.django.test/launch/'
                response = oidc_login.redirect(launch_url)

                # check cookie data
                self.assertEqual(len(response.cookies), 1)
                self.assertTrue(('lti1p3-state-' + uuid_val) in response.cookies)
                self.assertEqual(response.cookies['lti1p3-state-' + uuid_val]['value'], 'state-' + uuid_val)

                # check session data
                self.assertEqual(len(request.session), 1)
                self.assertEqual(request.session['lti1p3-nonce-' + uuid_val], True)

                # check redirect_url
                redirect_url = response.data
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

    def _get_django_launch_obj(self, request, tool_conf):
        from pylti1p3.contrib.django import DjangoMessageLaunch
        obj = DjangoMessageLaunch(request, tool_conf)
        return obj

    def _get_django_launch_cls(self):
        from pylti1p3.contrib.django import DjangoMessageLaunch
        return DjangoMessageLaunch
