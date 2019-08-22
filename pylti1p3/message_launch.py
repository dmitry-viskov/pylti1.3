import base64
import json
import string  # pylint: disable=deprecated-module
import uuid
from abc import ABCMeta, abstractmethod
import jwt
import requests
from jwcrypto.jwk import JWK

from .assignments_grades import AssignmentsGradesService
from .deep_link import DeepLink
from .exception import LtiException
from .message_validators import get_validators
from .names_roles import NamesRolesProvisioningService
from .service_connector import ServiceConnector


class MessageLaunch(object):
    __metaclass__ = ABCMeta
    _request = None
    _tool_config = None
    _session_service = None
    _cookie_service = None
    _jwt = None
    _jwt_verify_options = None
    _registration = None
    _launch_id = None
    _validated = False
    _auto_validation = True
    _restored = False

    def __init__(self, request, tool_config, session_service, cookie_service):
        self._request = request
        self._tool_config = tool_config
        self._session_service = session_service
        self._cookie_service = cookie_service
        self._launch_id = "lti1p3-launch-" + str(uuid.uuid4())
        self._jwt = {}
        self._jwt_verify_options = {'verify_aud': False}
        self._validated = False
        self._auto_validation = True
        self._restored = False

    @abstractmethod
    def _get_request_param(self, key):
        raise NotImplementedError

    def set_launch_id(self, launch_id):
        self._launch_id = launch_id
        return self

    def set_auto_validation(self, enable):
        self._auto_validation = enable
        return self

    def set_jwt(self, val):
        self._jwt = val
        return self

    def set_jwt_verify_options(self, val):
        self._jwt_verify_options = val
        return self

    def set_restored(self):
        self._restored = True
        return self

    def get_session_service(self):
        return self._session_service

    @classmethod
    def from_cache(cls, launch_id, request, tool_config, session_service=None, cookie_service=None):
        obj = cls(request, tool_config, session_service=session_service, cookie_service=cookie_service)
        launch_data = obj.get_session_service().get_launch_data(launch_id)
        return obj.set_launch_id(launch_id)\
            .set_auto_validation(enable=False)\
            .set_jwt({'body': launch_data})\
            .set_restored()\
            .validate_registration()

    def validate(self):
        """
        Validates all aspects of an incoming LTI message launch and caches the launch if successful.
        """
        if self._restored:
            raise LtiException("Can't validate restored launch")
        self._validated = True
        try:
            return self.validate_state()\
                .validate_jwt_format()\
                .validate_nonce()\
                .validate_registration()\
                .validate_jwt_signature()\
                .validate_deployment()\
                .validate_message()\
                .save_launch_data()
        except Exception:
            self._validated = False
            raise

    def _get_jwt_body(self):
        if not self._validated and self._auto_validation:
            self.validate()
        return self._jwt.get('body', {})

    def _get_iss(self):
        iss = self._get_jwt_body().get('iss')
        if not iss:
            raise LtiException('"iss" is empty')
        return iss

    def _get_id_token(self):
        id_token = self._get_request_param('id_token')
        if not id_token:
            raise LtiException("Missing id_token")
        return id_token

    def _get_deployment_id(self):
        deployment_id = self._get_jwt_body().get('https://purl.imsglobal.org/spec/lti/claim/deployment_id')
        if not deployment_id:
            raise LtiException("deployment_id is not set in jwt body")
        return deployment_id

    def has_nrps(self):
        """
        Returns whether or not the current launch can use the names and roles service.

        :return: bool  Returns a boolean indicating the availability of names and roles.
        """
        return self._get_jwt_body().get('https://purl.imsglobal.org/spec/lti-nrps/claim/namesroleservice', {})\
            .get('context_memberships_url', None) is not None

    def get_nrps(self):
        """
        Fetches an instance of the names and roles service for the current launch.

        :return: NamesRolesProvisioningService
        """
        connector = ServiceConnector(self._registration)
        names_role_service = self._get_jwt_body()\
            .get('https://purl.imsglobal.org/spec/lti-nrps/claim/namesroleservice')
        if not names_role_service:
            raise LtiException('namesroleservice is not set in jwt body')
        return NamesRolesProvisioningService(connector, names_role_service)

    def has_ags(self):
        """
        Returns whether or not the current launch can use the assignments and grades service.

        :return: bool  Returns a boolean indicating the availability of assignments and grades.
        """
        return self._get_jwt_body().get('https://purl.imsglobal.org/spec/lti-ags/claim/endpoint', None) is not None

    def get_ags(self):
        """
        Fetches an instance of the assignments and grades service for the current launch.

        :return: AssignmentsGradesService
        """
        connector = ServiceConnector(self._registration)
        endpoint = self._get_jwt_body() \
            .get('https://purl.imsglobal.org/spec/lti-ags/claim/endpoint')
        if not endpoint:
            raise LtiException('endpoint is not set in jwt body')
        return AssignmentsGradesService(connector, endpoint)

    def get_deep_link(self):
        """
        Fetches a deep link that can be used to construct a deep linking response.

        :return: DeepLink
        """
        deployment_id = self._get_deployment_id()
        deep_linking_settings = self._get_jwt_body() \
            .get('https://purl.imsglobal.org/spec/lti-dl/claim/deep_linking_settings')
        if not deep_linking_settings:
            raise LtiException('deep_linking_settings is not set in jwt body')

        return DeepLink(self._registration, deployment_id, deep_linking_settings)

    def is_deep_link_launch(self):
        """
        Returns whether or not the current launch is a deep linking launch.

        :return: bool  Returns true if the current launch is a deep linking launch.
        """
        return self._get_jwt_body() \
                   .get('https://purl.imsglobal.org/spec/lti/claim/message_type', None) == 'LtiDeepLinkingRequest'

    def is_resource_launch(self):
        """
        Returns whether or not the current launch is a resource launch.

        :return: bool  Returns true if the current launch is a resource launch.
        """
        return self._get_jwt_body() \
                   .get('https://purl.imsglobal.org/spec/lti/claim/message_type', None) == 'LtiResourceLinkRequest'

    def get_launch_data(self):
        """
        Fetches the decoded body of the JWT used in the current launch.

        :return: dict  Returns the decoded json body of the launch
        """
        return self._get_jwt_body()

    def get_launch_id(self):
        """
        Get the unique launch id for the current launch.

        :return: str  A unique identifier used to re-reference the current launch in subsequent requests.
        """
        return self._launch_id

    def urlsafe_b64decode(self, val):
        remainder = len(val) % 4
        if remainder > 0:
            padlen = 4 - remainder
            val = val + ('=' * padlen)
        if hasattr(str, 'maketrans'):
            tmp = val.translate(str.maketrans('-_', '+/'))
            return base64.b64decode(tmp).decode("utf-8")
        else:
            tmp = str(val).translate(string.maketrans('-_', '+/'))
            return base64.b64decode(tmp)

    def fetch_public_key(self, key_set_url):
        try:
            resp = requests.get(key_set_url)
        except requests.exceptions.RequestException as e:
            raise LtiException("Error during fetch URL " + key_set_url + ": " + str(e))
        try:
            return resp.json()
        except ValueError:
            raise LtiException("Invalid response from " + key_set_url + ". Must be JSON: " + resp.text)

    def get_public_key(self):
        public_key_set = self._registration.get_key_set()
        key_set_url = self._registration.get_key_set_url()

        if not public_key_set:
            if key_set_url.startswith(('http://', 'https://')):
                public_key_set = self.fetch_public_key(key_set_url)
                self._registration.set_key_set(public_key_set)
            else:
                raise LtiException("Invalid URL: " + key_set_url)

        # Find key used to sign the JWT (matches the KID in the header)
        kid = self._jwt.get('header', {}).get('kid', None)
        alg = self._jwt.get('header', {}).get('alg', None)

        if not kid:
            raise LtiException("JWT KID not found")
        if not alg:
            raise LtiException("JWT ALG not found")

        for key in public_key_set['keys']:
            key_kid = key.get('kid')
            key_alg = key.get('alg', 'RS256')
            if key_kid and key_kid == kid and key_alg == alg:
                try:
                    key_json = json.dumps(key)
                    jwk_obj = JWK.from_json(key_json)
                    return jwk_obj.export_to_pem()
                except (ValueError, TypeError):
                    raise LtiException("Can't convert JWT key to PEM format")

        # Could not find public key with a matching kid and alg.
        raise LtiException("Unable to find public key")

    def validate_state(self):
        # Check State for OIDC.
        state_from_request = self._get_request_param('state')
        if not state_from_request:
            raise LtiException("Missing state param")
        state_from_cookie = self._cookie_service.get_cookie(state_from_request)
        if state_from_request != state_from_cookie:
            # Error if state doesn't match.
            raise LtiException("State not found")

        return self

    def validate_jwt_format(self):
        id_token = self._get_id_token()
        jwt_parts = id_token.split('.')

        if len(jwt_parts) != 3:
            # Invalid number of parts in JWT.
            raise LtiException("Invalid id_token, JWT must contain 3 parts")

        try:
            # Decode JWT headers.
            header = self.urlsafe_b64decode(jwt_parts[0])
            self._jwt['header'] = json.loads(header)

            # Decode JWT body.
            body = self.urlsafe_b64decode(jwt_parts[1])
            self._jwt['body'] = json.loads(body)
        except Exception:
            raise LtiException("Invalid JWT format, can't be decoded")

        return self

    def validate_nonce(self):
        nonce = self._get_jwt_body().get('nonce')
        if not nonce:
            raise LtiException('"nonce" is empty')

        res = self._session_service.check_nonce(nonce)
        if not res:
            raise LtiException("Invalid Nonce")

        return self

    def validate_registration(self):
        iss = self._get_iss()

        # Find registration
        self._registration = self._tool_config.find_registration_by_issuer(iss)
        if not self._registration:
            raise LtiException('Registration not found.')

        # Check client id
        aud = self._get_jwt_body().get('aud')
        client_id = aud[0] if isinstance(aud, list) else aud
        if client_id != self._registration.get_client_id():
            raise LtiException("Client id not registered for this issuer")

        return self

    def validate_jwt_signature(self):
        id_token = self._get_id_token()

        # Fetch public key.
        public_key = self.get_public_key()

        try:
            jwt.decode(id_token, public_key, algorithms=['RS256'], options=self._jwt_verify_options)
        except jwt.InvalidTokenError as e:
            raise LtiException("Can't decode id_token: " + str(e))

        return self

    def validate_deployment(self):
        iss = self._get_iss()
        deployment_id = self._get_deployment_id()

        # Find deployment.
        deployment = self._tool_config.find_deployment(iss, deployment_id)
        if not deployment:
            raise LtiException("Unable to find deployment")

        return self

    def validate_message(self):
        jwt_body = self._get_jwt_body()
        message_type = jwt_body.get('https://purl.imsglobal.org/spec/lti/claim/message_type', None)
        if not message_type:
            raise LtiException("Invalid message type")

        validators = get_validators()
        validated = False
        for validator in validators:
            if validator.can_validate(jwt_body):
                if validated:
                    raise LtiException("Validator conflict")
                validated = True
                res = validator.validate(jwt_body)
                if not res:
                    raise LtiException("Message validation failed")

        if not validated:
            raise LtiException("Unrecognized message type")

        return self

    def save_launch_data(self):
        self._session_service.save_launch_data(self._launch_id, self._jwt['body'])
        return self

    def get_params_from_login(self):
        state = self._get_request_param('state')
        return self._session_service.get_state_params(state)
