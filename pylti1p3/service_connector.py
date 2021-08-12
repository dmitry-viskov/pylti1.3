import hashlib
import re
import sys
import time
import typing as t
import uuid

import jwt  # type: ignore
import requests

from .exception import LtiServiceException

if t.TYPE_CHECKING:
    from mypy_extensions import TypedDict
    from .registration import Registration

    _ServiceConnectorResponse = TypedDict('_ServiceConnectorResponse', {
        'headers': t.Union[t.Dict[str, str], t.MutableMapping[str, str]],
        'body': t.Union[None, int, float, t.List[object], t.Dict[str, object], str],
        'next_page_url': t.Optional[str]
    })


class ServiceConnector(object):
    _registration = None  # type: Registration
    _access_tokens = None  # type: t.Dict[str, str]

    def __init__(self, registration):
        # type: (Registration) -> None
        self._registration = registration
        self._access_tokens = {}

    def get_access_token(self, scopes):
        # type: (t.Sequence[str]) -> str

        # Don't fetch the same key more than once
        scopes = sorted(scopes)
        scopes_str = '|'.join(scopes)  # type: str

        if sys.version_info[0] > 2:
            scopes_bytes = scopes_str.encode('utf-8')
        else:
            scopes_bytes = scopes_str
        scope_key = hashlib.md5(scopes_bytes).hexdigest()

        if scope_key in self._access_tokens:
            return self._access_tokens[scope_key]

        # Build up JWT to exchange for an auth token
        client_id = self._registration.get_client_id()
        auth_url = self._registration.get_auth_token_url()
        assert auth_url is not None, 'auth_url should be set at this point'
        auth_audience = self._registration.get_auth_audience()
        aud = auth_audience if auth_audience else auth_url

        jwt_claim = {
            "iss": client_id,
            "sub": client_id,
            "aud": aud,
            "iat": int(time.time()) - 5,
            "exp": int(time.time()) + 60,
            "jti": 'lti-service-token-' + str(uuid.uuid4())
        }
        headers = None
        kid = self._registration.get_kid()
        if kid:
            headers = {'kid': kid}

        # Sign the JWT with our private key (given by the platform on registration)
        private_key = self._registration.get_tool_private_key()
        assert private_key is not None, 'Private key should be set at this point'
        jwt_val = self.encode_jwt(jwt_claim, private_key, headers)

        auth_request = {
            'grant_type': 'client_credentials',
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': jwt_val,
            'scope': ' '.join(scopes)
        }

        # Make request to get auth token
        r = requests.post(auth_url, data=auth_request)
        if not r.ok:
            raise LtiServiceException(r)
        response = r.json()

        self._access_tokens[scope_key] = response['access_token']
        return self._access_tokens[scope_key]

    def encode_jwt(self, message, private_key, headers):
        jwt_val = jwt.encode(message, private_key, algorithm='RS256', headers=headers)
        if sys.version_info[0] > 2 and isinstance(jwt_val, bytes):
            return jwt_val.decode('utf-8')
        return jwt_val

    def make_service_request(
            self,
            scopes,  # type: t.Sequence[str]
            url,  # type: str
            is_post=False,  # type: bool
            data=None,  # type: t.Union[None, str]
            content_type='application/json',  # type: str
            accept='application/json',  # type: str
            case_insensitive_headers=False,  # type: bool
    ):
        # type: (...) -> _ServiceConnectorResponse
        access_token = self.get_access_token(scopes)
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Accept': accept
        }

        if is_post:
            headers['Content-Type'] = content_type
            post_data = data or None
            r = requests.post(url, data=post_data, headers=headers)
        else:
            r = requests.get(url, headers=headers)

        if not r.ok:
            raise LtiServiceException(r)

        next_page_url = None
        link_header = r.headers.get('link', '')
        if link_header:
            match = re.search(r'<([^>]*)>;\s*rel="next"', link_header.replace('\n', ' ').lower().strip())
            if match:
                next_page_url = match.group(1)

        return {
            'headers': r.headers if case_insensitive_headers else dict(r.headers),
            'body': r.json() if r.content else None,
            'next_page_url': next_page_url if next_page_url else None
        }
