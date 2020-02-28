import json
import unittest
import requests_mock

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
from .request import DjangoFakeRequest
from .response import DjangoFakeResponse
from .tool_config import get_test_tool_conf, TOOL_CONFIG


class TestLinkBase(unittest.TestCase):
    iss = 'replace-me'
    get_login_data = {}
    post_login_data = {}

    def _make_oidc_login(self, uuid_val=None, tool_conf_cls=None):
        tool_conf = get_test_tool_conf(tool_conf_cls)
        request = None
        login_data = {}
        if not uuid_val:
            uuid_val = 'test-uuid-1234'

        if self.get_login_data:
            request = DjangoFakeRequest(get=self.get_login_data)
            login_data = self.get_login_data.copy()
        elif self.post_login_data:
            request = DjangoFakeRequest(post=self.post_login_data)
            login_data = self.post_login_data.copy()

        with patch('django.shortcuts.redirect') as mock_redirect:
            from pylti1p3.contrib.django import DjangoOIDCLogin
            with patch.object(DjangoOIDCLogin, "_get_uuid", autospec=True) as get_uuid:
                get_uuid.side_effect = lambda x: uuid_val  # pylint: disable=unnecessary-lambda
                oidc_login = DjangoOIDCLogin(request, tool_conf)
                mock_redirect.side_effect = lambda x: DjangoFakeResponse(x)  # pylint: disable=unnecessary-lambda
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

    def _launch(self, request, tool_conf, key_set_url_response=None, force_validation=False):
        from pylti1p3.contrib.django import DjangoMessageLaunch
        obj = DjangoMessageLaunch(request, tool_conf)
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
        from pylti1p3.contrib.django import DjangoMessageLaunch
        with patch.object(DjangoMessageLaunch, "_get_jwt_body", autospec=True) as get_jwt_body:
            get_jwt_body.side_effect = side_effect
            return self._launch(request, tool_conf, force_validation=True)


class TestServicesBase(unittest.TestCase):
    jwt_body = {
        'iss': 'https://canvas.instructure.com',
        'aud': '10000000000004',
        'sub': 'a445ca99-1a64-4697-9bfa-508a118245ea',
        'https://purl.imsglobal.org/spec/lti-nrps/claim/namesroleservice': {
            'context_memberships_url': 'http://canvas.docker/api/lti/courses/1/names_and_roles',
            'service_versions': ['2.0'],
            'errors': {'errors': {}},
            'validation_context': None
        },
        'https://purl.imsglobal.org/spec/lti-ags/claim/endpoint': {
            'scope': ['https://purl.imsglobal.org/spec/lti-ags/scope/score',
                      'https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly',
                      'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly',
                      'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem'],
            'lineitems': 'http://canvas.docker/api/lti/courses/1/line_items',
            'errors': {'errors': {}},
            'validation_context': None
        }
    }

    def _get_auth_token_url(self):
        return TOOL_CONFIG[self.jwt_body['iss']]['auth_token_url']

    def _get_auth_token_response(self):
        return {
            'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwcz'
                            'ovL2NhbnZhcy5pbnN0cnVjdHVyZS5jb20iLCJzdWI'
                            'iOiIxMDAwMDAwMDAwMDAwNCIsImF1ZCI6Imh0dHA6Ly9jYW52YXMuZG'
                            '9ja2VyL2xvZ2luL29hdXRoMi90b2tlbiIsImlhdCI'
                            '6MTU2NTYwNDc3NiwiZXhwIjoxNTY1NjA4Mzc2LCJqdGkiOiIyZTg1Nz'
                            'ZkYi0wODhkLTQ1ZjUtYTBhMC03YzE2NzI4NjA2Zjg'
                            'iLCJzY29wZXMiOiJodHRwczovL3B1cmwuaW1zZ2xvYmFsLm9yZy9zcG'
                            'VjL2x0aS1hZ3Mvc2NvcGUvbGluZWl0ZW0gaHR0cHM'
                            '6Ly9wdXJsLmltc2dsb2JhbC5vcmcvc3BlYy9sdGktYWdzL3Njb3BlL2'
                            'xpbmVpdGVtLnJlYWRvbmx5IGh0dHBzOi8vcHVybC5'
                            'pbXNnbG9iYWwub3JnL3NwZWMvbHRpLWFncy9zY29wZS9yZXN1bHQucm'
                            'VhZG9ubHkgaHR0cHM6Ly9wdXJsLmltc2dsb2JhbC5'
                            'vcmcvc3BlYy9sdGktYWdzL3Njb3BlL3Njb3JlIn0.GdRwhYsmxEENWY'
                            'iqFOdpcKRgrHCl0Wb1-GuBb-qXqms',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': 'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem '
                     'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly '
                     'https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly '
                     'https://purl.imsglobal.org/spec/lti-ags/scope/score'
        }

    def _get_jwt_body(self):
        return self.jwt_body
