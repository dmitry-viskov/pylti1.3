import json
import unittest
import requests_mock

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from .django_mixin import DjangoMixin
from .flask_mixin import FlaskMixin
from .tool_config import TOOL_CONFIG


class TestLinkBase(DjangoMixin, FlaskMixin, unittest.TestCase):
    iss = 'replace-me'
    get_login_data = {}
    post_login_data = {}

    def _make_oidc_login(self, adapter=None, uuid_val=None, tool_conf_cls=None, secure=False):
        if adapter == 'flask':
            return self._make_flask_oidc_login(uuid_val, tool_conf_cls, secure)
        else:
            return self._make_django_oidc_login(uuid_val, tool_conf_cls)

    def _get_request(self, login_request, login_response, request_is_secure=False, empty_session=False,
                     empty_cookies=False, post_data=None, adapter=None):
        if adapter == 'flask':
            return self._get_flask_request(login_request, login_response, request_is_secure, post_data,
                                           empty_session, empty_cookies)
        else:
            return self._get_django_request(login_request, login_response, post_data, empty_session, empty_cookies)

    def _launch(self, request, tool_conf, key_set_url_response=None, force_validation=False, adapter=None):
        if adapter == 'flask':
            obj = self._get_flask_launch_obj(request, tool_conf)
        else:
            obj = self._get_django_launch_obj(request, tool_conf)
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

    def _launch_with_invalid_jwt_body(self, side_effect, request, tool_conf, adapter=None):
        if adapter == 'flask':
            klass = self._get_flask_launch_cls()
        else:
            klass = self._get_django_launch_cls()
        with patch.object(klass, "_get_jwt_body", autospec=True) as get_jwt_body:
            get_jwt_body.side_effect = side_effect
            return self._launch(request, tool_conf, force_validation=True, adapter=adapter)


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
