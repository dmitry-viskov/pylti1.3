import hashlib
import time
import sys
import uuid
import jwt
import requests

from .exception import LtiException


class ServiceConnector(object):
    _registration = None
    _access_tokens = None

    def __init__(self, registration):
        self._registration = registration
        self._access_tokens = {}

    def get_access_token(self, scopes):
        # Don't fetch the same key more than once
        scopes = sorted(scopes)
        scopes_str = '|'.join(scopes)

        if sys.version_info[0] > 2:
            scopes_str = scopes_str.encode('utf-8')
        scope_key = hashlib.md5(scopes_str).hexdigest()

        if scope_key in self._access_tokens:
            return self._access_tokens[scope_key]

        # Build up JWT to exchange for an auth token
        iss = self._registration.get_issuer()
        client_id = self._registration.get_client_id()
        auth_url = self._registration.get_auth_token_url()

        jwt_claim = {
            "iss": iss,
            "sub": client_id,
            "aud": auth_url,
            "iat": int(time.time()) - 5,
            "exp": int(time.time()) + 60,
            "jti": 'lti-service-token-' + str(uuid.uuid4())
        }

        # Sign the JWT with our private key (given by the platform on registration)
        jwt_val = jwt.encode(jwt_claim, self._registration.get_tool_private_key(), algorithm='RS256')

        auth_request = {
            'grant_type': 'client_credentials',
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': jwt_val,
            'scope': ' '.join(scopes)
        }

        # Make request to get auth token
        r = requests.post(auth_url, data=auth_request)
        if r.status_code not in (200, 201):
            raise LtiException('HTTP response [%s]: %s - %s' % (auth_url, str(r.status_code), r.text))
        response = r.json()

        self._access_tokens[scope_key] = response['access_token']
        return self._access_tokens[scope_key]

    def make_service_request(self, scopes, url, is_post=False, data=None, content_type='application/json',
                             accept='application/json'):
        access_token = self.get_access_token(scopes)
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Accept': accept
        }

        if is_post:
            headers['Content-Type'] = content_type
            post_data = str(data) if data else None
            r = requests.post(url, data=post_data, headers=headers)
        else:
            r = requests.get(url, headers=headers)

        if r.status_code not in (200, 201):
            raise LtiException('HTTP response [%s]: %s - %s' % (url, str(r.status_code), r.text))

        return {
            'headers': dict(r.headers),
            'body': r.json() if r.content else None
        }
