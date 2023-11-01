import hashlib
import re
import time
import typing as t
import uuid

import jwt  # type: ignore
import requests
import typing_extensions as te
from .exception import LtiException, LtiServiceException
from .registration import Registration

TServiceConnectorResponse = te.TypedDict(
    "TServiceConnectorResponse",
    {
        "headers": t.Union[t.Dict[str, str], t.MutableMapping[str, str]],
        "body": t.Union[None, int, float, t.List[object], t.Dict[str, object], str],
        "next_page_url": t.Optional[str],
    },
)


REQUESTS_USER_AGENT = "PyLTI1p3-client"


class ServiceConnector:
    _registration: Registration
    _access_tokens: t.Dict[str, str]

    def __init__(
        self,
        registration: Registration,
        requests_session: t.Optional[requests.Session] = None,
    ):
        self._registration = registration
        self._access_tokens = {}
        if requests_session:
            self._requests_session = requests_session
        else:
            self._requests_session = requests.Session()
            self._requests_session.headers["User-Agent"] = REQUESTS_USER_AGENT

    def get_access_token(self, scopes: t.Sequence[str]) -> str:
        # Don't fetch the same key more than once
        scopes = sorted(scopes)
        scopes_str: str = "|".join(scopes)
        scopes_bytes = scopes_str.encode("utf-8")

        scope_key = hashlib.md5(scopes_bytes).hexdigest()

        if scope_key in self._access_tokens:
            return self._access_tokens[scope_key]

        # Build up JWT to exchange for an auth token
        client_id = self._registration.get_client_id()
        assert client_id is not None, "client_id should be set at this point"
        auth_url = self._registration.get_auth_token_url()
        assert auth_url is not None, "auth_url should be set at this point"
        auth_audience = self._registration.get_auth_audience()
        aud = auth_audience if auth_audience else auth_url

        jwt_claim: t.Dict[str, t.Union[str, int]] = {
            "iss": str(client_id),
            "sub": str(client_id),
            "aud": str(aud),
            "iat": int(time.time()) - 5,
            "exp": int(time.time()) + 60,
            "jti": "lti-service-token-" + str(uuid.uuid4()),
        }
        headers = {}
        kid = self._registration.get_kid()
        if kid:
            headers = {"kid": kid}

        # Sign the JWT with our private key (given by the platform on registration)
        private_key = self._registration.get_tool_private_key()
        assert private_key is not None, "Private key should be set at this point"
        jwt_val = self.encode_jwt(jwt_claim, private_key, headers)

        auth_request = {
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": jwt_val,
            "scope": " ".join(scopes),
        }

        # Make request to get auth token
        r = self._requests_session.post(auth_url, data=auth_request)
        if not r.ok:
            raise LtiServiceException(r)
        response = r.json()

        self._access_tokens[scope_key] = response["access_token"]
        return self._access_tokens[scope_key]

    def encode_jwt(
        self,
        message: t.Dict[str, t.Union[str, int]],
        private_key: str,
        headers: t.Dict[str, str],
    ) -> str:
        jwt_val = jwt.encode(message, private_key, algorithm="RS256", headers=headers)
        if isinstance(jwt_val, bytes):
            return jwt_val.decode("utf-8")
        return jwt_val

    def make_service_request(
        self,
        scopes: t.Sequence[str],
        url: str,
        method: str = 'GET',
        data: t.Optional[str] = None,
        content_type: str = "application/json",
        accept: str = "application/json",
        case_insensitive_headers: bool = False,
    ) -> TServiceConnectorResponse:
        access_token = self.get_access_token(scopes)
        headers = {"Authorization": "Bearer " + access_token, "Accept": accept}

        if method == 'GET':
            r = self._requests_session.get(url, headers=headers)
        elif method == 'DELETE':
            r = self._requests_session.delete(url, headers=headers)
        else:
            headers["Content-Type"] = content_type
            request_data = data or None
            if method == 'PUT':
                r = self._requests_session.put(url, data=request_data, headers=headers)
            elif method == 'POST':
                r = self._requests_session.post(url, data=request_data, headers=headers)
            else:
                raise LtiException(f'Unsupported method: {method}. Available methods are: '
                                   '"GET", "PUT", "POST", "DELETE".')

        if not r.ok:
            raise LtiServiceException(r)

        next_page_url = None
        link_header = r.headers.get("link", "")
        if link_header:
            match = re.search(
                r'<([^>]*)>;\s*rel="next"',
                link_header.replace("\n", " ").lower().strip(),
            )
            if match:
                next_page_url = match.group(1)

        return {
            "headers": r.headers if case_insensitive_headers else dict(r.headers),
            "body": r.json() if r.content else None,
            "next_page_url": next_page_url if next_page_url else None,
        }
