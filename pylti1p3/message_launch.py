import base64
import hashlib
import json
import string  # pylint: disable=deprecated-module
import typing as t
import uuid
from abc import ABCMeta, abstractmethod

import jwt  # type: ignore
import requests
from jwcrypto.jwk import JWK  # type: ignore

from .actions import Action
from .assignments_grades import AssignmentsGradesService
from .deep_link import DeepLink
from .exception import LtiException
from .launch_data_storage.base import DisableSessionId
from .message_validators import get_validators
from .message_validators.deep_link import DeepLinkMessageValidator
from .message_validators.privacy_launch import PrivacyLaunchValidator
from .message_validators.resource_message import ResourceMessageValidator
from .names_roles import NamesRolesProvisioningService
from .roles import StaffRole, StudentRole, TeacherRole, TeachingAssistantRole, DesignerRole, ObserverRole, \
    TransientRole
from .service_connector import ServiceConnector
from .utils import encode_on_py3

if t.TYPE_CHECKING:
    from .launch_data_storage.base import LaunchDataStorage
    from .registration import Registration, _KeySet
    from .request import Request
    from .tool_config import ToolConfAbstract  # pylint: disable=cyclic-import
    from .session import SessionService
    from .cookie import CookieService
    from .deep_link import _DeepLinkData
    from .names_roles import _NamesAndRolesData
    from .assignments_grades import _AssignmentsGradersData

    from mypy_extensions import TypedDict
    from typing_extensions import Literal

    _ResourceLinkClaim = TypedDict('_ResourceLinkClaim', {
        # Required data
        'id': str,

        # Optional data
        'description': str,
        'title': str,
    }, total=False)

    _ContextClaim = TypedDict('_ContextClaim', {
        # Required data
        'id': str,

        # Optional data
        'label': str,
        'title': str,
        'type': t.List[str],
    }, total=False)

    _ToolPlatformClaim = TypedDict('_ToolPlatformClaim', {
        # Required data
        'guid': str,

        # Optional data
        'contact_email': str,
        'description': str,
        'name': str,
        'url': str,
        'product_family_code': str,
        'version': str,
    }, total=False)

    _LearningInformationServicesClaim = TypedDict('_LearningInformationServicesClaim', {
        'person_sourcedid': str,
        'course_offering_sourcedid': str,
        'course_section_sourcedid': str,
    }, total=False)

    _MigrationClaim = TypedDict(
        '_MigrationClaim', {
            # Required data
            'oauth_consumer_key': str,

            # Optional data
            'oauth_consumer_key_sign': str,
            'user_id': str,
            'context_id': str,
            'tool_consumer_instance_guid ': str,
            'resource_link_id': str,
        },
        total=False,
    )

    _ForUserClaim = TypedDict(
        '_ForUserClaim', {
            # Required data
            'id': str,

            # Optional data
            'person_sourcedId': str,
            'given_name': str,
            'family_name': str,
            'name': str,
            'email': str,
            'roles': t.List[str]
        }
    )

    _LaunchData = TypedDict(
        '_LaunchData', {
            # Required data
            'iss': str,
            'nonce': str,
            'aud': t.Union[t.List[str], str],
            'https://purl.imsglobal.org/spec/lti/claim/message_type':
                Literal['LtiResourceLinkRequest', 'LtiDeepLinkingRequest', 'DataPrivacyLaunchRequest'],
            'https://purl.imsglobal.org/spec/lti/claim/version': Literal['1.3.0'],
            'https://purl.imsglobal.org/spec/lti/claim/deployment_id': str,
            'https://purl.imsglobal.org/spec/lti/claim/target_link_uri': str,
            'https://purl.imsglobal.org/spec/lti/claim/resource_link': _ResourceLinkClaim,
            'https://purl.imsglobal.org/spec/lti/claim/roles': t.List[str],
            'sub': str,

            # Optional data
            'given_name': str,
            'family_name': str,
            'name': str,
            'email': str,
            'https://purl.imsglobal.org/spec/lti/claim/context': _ContextClaim,
            'https://purl.imsglobal.org/spec/lti/claim/lis': _LearningInformationServicesClaim,
            'https://purl.imsglobal.org/spec/lti/claim/custom': t.Mapping[str, str],
            'https://purl.imsglobal.org/spec/lti-dl/claim/deep_linking_settings': _DeepLinkData,
            'https://purl.imsglobal.org/spec/lti-nrps/claim/namesroleservice': _NamesAndRolesData,
            'https://purl.imsglobal.org/spec/lti-ags/claim/endpoint': _AssignmentsGradersData,
            'https://purl.imsglobal.org/spec/lti/claim/tool_platform': _ToolPlatformClaim,
            'https://purl.imsglobal.org/spec/lti/claim/role_scope_mentor': t.List[str],
            'https://purl.imsglobal.org/spec/lti/claim/lti1p1': _MigrationClaim,
            'https://purl.imsglobal.org/spec/lti/claim/for_user': _ForUserClaim
        },
        total=False
    )

    _JwtHeader = TypedDict(
        '_JwtHeader', {
            'kid': str,
            'alg': str,
        },
        total=False,
    )

    _JwtData = TypedDict(
        '_JwtData', {
            'header': _JwtHeader,
            'body': _LaunchData,
        },
        total=False
    )


REQ = t.TypeVar('REQ', bound='Request')
TCONF = t.TypeVar('TCONF', bound='ToolConfAbstract')
SES = t.TypeVar('SES', bound='SessionService')
COOK = t.TypeVar('COOK', bound='CookieService')
T_SELF = t.TypeVar('T_SELF', bound='MessageLaunch')


class MessageLaunch(t.Generic[REQ, TCONF, SES, COOK]):
    __metaclass__ = ABCMeta
    _request = None  # type: REQ
    _tool_config = None  # type: TCONF
    _session_service = None  # type: SES
    _cookie_service = None  # type: COOK
    _jwt = None  # type: _JwtData
    _jwt_verify_options = None  # type: t.Dict[str, bool]
    _registration = None  # type: t.Optional[Registration]
    _launch_id = None  # type: str
    _validated = False  # type: bool
    _auto_validation = True  # type: bool
    _restored = False  # type: bool
    _id_token_hash = None  # type: t.Optional[str]
    _public_key_cache_data_storage = None  # type: t.Optional[LaunchDataStorage[t.Any]]
    _public_key_cache_lifetime = None  # type: t.Optional[int]

    def __init__(self, request, tool_config, session_service, cookie_service, launch_data_storage=None):
        # type: (REQ, TCONF, SES, COOK, t.Optional[LaunchDataStorage[t.Any]]) -> None
        self._request = request
        self._tool_config = tool_config
        self._session_service = session_service
        self._cookie_service = cookie_service
        self._launch_id = "lti1p3-launch-" + str(uuid.uuid4())
        self._jwt = {}
        self._jwt_verify_options = {'verify_aud': False}
        self._id_token_hash = None
        self._validated = False
        self._auto_validation = True
        self._restored = False
        self._public_key_cache_data_storage = None
        self._public_key_cache_lifetime = None

        if launch_data_storage:
            self.set_launch_data_storage(launch_data_storage)

    @abstractmethod
    def _get_request_param(self, key):
        # type: (str) -> t.Any
        raise NotImplementedError

    def set_launch_id(self, launch_id):
        # type: (T_SELF, str) -> T_SELF
        self._launch_id = launch_id
        return self

    def set_auto_validation(self, enable):
        # type: (T_SELF, bool) -> T_SELF
        self._auto_validation = enable
        return self

    def set_jwt(self, val):
        # type: (T_SELF, _JwtData) -> T_SELF
        self._jwt = val
        return self

    def set_jwt_verify_options(self, val):
        # type: (T_SELF, t.Dict[str, bool]) -> T_SELF
        self._jwt_verify_options = val
        return self

    def set_restored(self):
        # type: (T_SELF) -> T_SELF
        self._restored = True
        return self

    def get_session_service(self):
        # type: () -> SES
        return self._session_service

    def get_iss(self):
        # type: () -> str
        iss = self._get_jwt_body().get('iss')
        if not iss:
            raise LtiException('"iss" is empty')
        return iss

    def get_client_id(self):
        # type: () -> str
        jwt_body = self._get_jwt_body()
        aud = jwt_body.get('aud')
        return aud[0] if isinstance(aud, list) else aud  # type: ignore

    @classmethod
    def from_cache(cls, launch_id, request, tool_config, session_service=None, cookie_service=None,
                   launch_data_storage=None):
        # type: (t.Type[T_SELF], str, REQ, TCONF, SES, COOK, t.Optional[LaunchDataStorage[t.Any]]) -> T_SELF
        obj = cls(request, tool_config, session_service=session_service, cookie_service=cookie_service,
                  launch_data_storage=launch_data_storage)
        launch_data = obj.get_session_service().get_launch_data(launch_id)
        if not launch_data:
            raise LtiException("Launch data not found")
        return obj.set_launch_id(launch_id)\
            .set_auto_validation(enable=False)\
            .set_jwt({'body': launch_data})\
            .set_restored()\
            .validate_registration()

    def validate(self):
        # type: (T_SELF) -> T_SELF
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
        # type: () -> _LaunchData
        if not self._validated and self._auto_validation:
            self.validate()
        return self._jwt.get('body', {})

    def _get_iss(self):
        # type: () -> str
        iss = self._get_jwt_body().get('iss')
        if not iss:
            raise LtiException('"iss" is empty')
        return iss

    def _get_id_token(self):
        # type: () -> str
        id_token = self._get_request_param('id_token')
        if not id_token:
            raise LtiException("Missing id_token")
        return id_token

    def _get_id_token_hash(self):
        # type: () -> str
        if not self._id_token_hash:
            id_token = self._get_id_token()
            id_token_param = encode_on_py3(id_token, 'utf8')
            self._id_token_hash = hashlib.md5(id_token_param).hexdigest()
        return self._id_token_hash

    def _get_deployment_id(self):
        # type: () -> str
        deployment_id = self._get_jwt_body().get('https://purl.imsglobal.org/spec/lti/claim/deployment_id')
        if not deployment_id:
            raise LtiException("deployment_id is not set in jwt body")
        return deployment_id

    def has_nrps(self):
        # type: () -> bool
        """
        Returns whether or not the current launch can use the names and roles service.

        :return: bool  Returns a boolean indicating the availability of names and roles.
        """
        return self._get_jwt_body().get('https://purl.imsglobal.org/spec/lti-nrps/claim/namesroleservice', {})\
            .get('context_memberships_url', None) is not None

    def get_nrps(self):
        # type: () -> NamesRolesProvisioningService
        """
        Fetches an instance of the names and roles service for the current launch.

        :return: NamesRolesProvisioningService
        """
        assert self._registration is not None, 'Registration not yet set'
        connector = ServiceConnector(self._registration)
        names_role_service = self._get_jwt_body()\
            .get('https://purl.imsglobal.org/spec/lti-nrps/claim/namesroleservice')
        if not names_role_service:
            raise LtiException('namesroleservice is not set in jwt body')
        return NamesRolesProvisioningService(connector, names_role_service)

    def has_ags(self):
        # type: () -> bool
        """
        Returns whether or not the current launch can use the assignments and grades service.

        :return: bool  Returns a boolean indicating the availability of assignments and grades.
        """
        return self._get_jwt_body().get('https://purl.imsglobal.org/spec/lti-ags/claim/endpoint', None) is not None

    def get_ags(self):
        # type: () -> AssignmentsGradesService
        """
        Fetches an instance of the assignments and grades service for the current launch.

        :return: AssignmentsGradesService
        """
        assert self._registration is not None, 'Registration not yet set'
        connector = ServiceConnector(self._registration)
        endpoint = self._get_jwt_body() \
            .get('https://purl.imsglobal.org/spec/lti-ags/claim/endpoint')
        if not endpoint:
            raise LtiException('endpoint is not set in jwt body')
        return AssignmentsGradesService(connector, endpoint)

    def get_deep_link(self):
        # type: () -> DeepLink
        """
        Fetches a deep link that can be used to construct a deep linking response.

        :return: DeepLink
        """
        assert self._registration is not None, 'Registration not yet set'

        deployment_id = self._get_deployment_id()
        deep_linking_settings = self._get_jwt_body() \
            .get('https://purl.imsglobal.org/spec/lti-dl/claim/deep_linking_settings')
        if not deep_linking_settings:
            raise LtiException('deep_linking_settings is not set in jwt body')

        return DeepLink(self._registration, deployment_id, deep_linking_settings)

    def get_data_privacy_launch_user(self):
        # type: () -> t.Optional[_ForUserClaim]
        """
        Applicable for DataPrivacyLaunchRequest only. Returns information about user
        who's data the launch is intended to action upon, for instance the student
        who has requested their data be removed under GDPR's right to be forgotten.

        :return: dict
        """
        jwt_body = self._get_jwt_body()
        return jwt_body.get('https://purl.imsglobal.org/spec/lti/claim/for_user')

    def is_deep_link_launch(self):
        # type: () -> bool
        """
        Returns whether or not the current launch is a deep linking launch.

        :return: bool  Returns true if the current launch is a deep linking launch.
        """
        jwt_body = self._get_jwt_body()
        return DeepLinkMessageValidator().can_validate(jwt_body)

    def is_resource_launch(self):
        # type: () -> bool
        """
        Returns whether or not the current launch is a resource launch.

        :return: bool  Returns true if the current launch is a resource launch.
        """
        jwt_body = self._get_jwt_body()
        return ResourceMessageValidator().can_validate(jwt_body)

    def is_data_privacy_launch(self):
        # type: () -> bool
        """
        Returns whether or not the current launch is a data privacy launch.

        :return: bool  Returns true if the current launch is a data privacy launch.
        """
        jwt_body = self._get_jwt_body()
        return PrivacyLaunchValidator().can_validate(jwt_body)

    def get_launch_data(self):
        # type: () -> _LaunchData
        """
        Fetches the decoded body of the JWT used in the current launch.

        :return: dict  Returns the decoded json body of the launch
        """
        return self._get_jwt_body()

    def get_launch_id(self):
        # type: () -> str
        """
        Get the unique launch id for the current launch.

        :return: str  A unique identifier used to re-reference the current launch in subsequent requests.
        """
        return self._launch_id

    def get_tool_conf(self):
        # type: () -> TCONF
        return self._tool_config

    def urlsafe_b64decode(self, val):
        # type: (str) -> str
        remainder = len(val) % 4
        if remainder > 0:
            padlen = 4 - remainder
            val = val + ('=' * padlen)
        if hasattr(str, 'maketrans'):
            tmp = val.translate(str.maketrans('-_', '+/'))  # type: ignore
            return base64.b64decode(tmp).decode("utf-8")  # type: ignore
        else:
            tmp = str(val).translate(string.maketrans('-_', '+/'))  # type: ignore
            return base64.b64decode(tmp)  # type: ignore

    def set_public_key_caching(self, data_storage, cache_lifetime=7200):
        # type: (LaunchDataStorage[t.Any], int) -> None
        self._public_key_cache_data_storage = data_storage
        self._public_key_cache_lifetime = cache_lifetime

    def fetch_public_key(self, key_set_url):
        # type: (str) -> _KeySet
        cache_key = 'key-set-url-' + hashlib.md5(encode_on_py3(key_set_url, 'utf-8')).hexdigest()

        with DisableSessionId(self._public_key_cache_data_storage):
            if self._public_key_cache_data_storage:
                public_key = self._public_key_cache_data_storage.get_value(cache_key)
                if public_key:
                    return public_key

            try:
                resp = requests.get(key_set_url)
            except requests.exceptions.RequestException as e:
                raise LtiException("Error during fetch URL " + key_set_url + ": " + str(e))
            try:
                public_key = resp.json()
                if self._public_key_cache_data_storage:
                    self._public_key_cache_data_storage.set_value(
                        cache_key, public_key, self._public_key_cache_lifetime)
                return public_key
            except ValueError:
                raise LtiException("Invalid response from " + key_set_url + ". Must be JSON: " + resp.text)

    def get_public_key(self):
        # type: () -> str
        assert self._registration is not None, 'Registration not yet set'
        public_key_set = self._registration.get_key_set()
        key_set_url = self._registration.get_key_set_url()

        if not public_key_set:
            assert key_set_url is not None, 'If public_key_set is not set, public_set_url should be set'
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
        # type: (T_SELF) -> T_SELF
        # Check State for OIDC.
        state_from_request = self._get_request_param('state')
        if not state_from_request:
            raise LtiException("Missing state param")

        id_token_hash = self._get_id_token_hash()
        if not self._session_service.check_state_is_valid(state_from_request, id_token_hash):
            state_from_cookie = self._cookie_service.get_cookie(state_from_request)
            if state_from_request != state_from_cookie:
                # Error if state doesn't match.
                raise LtiException("State not found")

        return self

    def validate_jwt_format(self):
        # type: (T_SELF) -> T_SELF
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
        # type: (T_SELF) -> T_SELF
        nonce = self._get_jwt_body().get('nonce')
        if not nonce:
            raise LtiException('"nonce" is empty')

        res = self._session_service.check_nonce(nonce)
        if not res:
            raise LtiException("Invalid Nonce")

        return self

    def validate_registration(self):
        # type: (T_SELF) -> T_SELF
        iss = self.get_iss()
        jwt_body = self._get_jwt_body()
        client_id = self.get_client_id()

        # Mypy doesn't support higher kinded types yet so it thinks that all
        # generic attrs have type `Any`. See issue:
        # https://github.com/python/mypy/issues/8228
        config = self._tool_config  # type: ToolConfAbstract[REQ]
        req = self._request  # type: REQ

        # Find registration
        if config.check_iss_has_one_client(iss):
            self._registration = config.find_registration(
                iss, action=Action.MESSAGE_LAUNCH, request=req, jwt_body=jwt_body)
        else:
            self._registration = config.find_registration_by_params(
                iss, client_id, action=Action.MESSAGE_LAUNCH, request=req, jwt_body=jwt_body)

        if not self._registration:
            raise LtiException('Registration not found.')

        # Check client id
        if client_id != self._registration.get_client_id():
            raise LtiException("Client id not registered for this issuer")

        return self

    def validate_jwt_signature(self):
        # type: (T_SELF) -> T_SELF
        id_token = self._get_id_token()

        # Fetch public key.
        public_key = self.get_public_key()

        try:
            jwt.decode(id_token, public_key, algorithms=['RS256'], options=self._jwt_verify_options)
        except jwt.InvalidTokenError as e:
            raise LtiException("Can't decode id_token: " + str(e))

        return self

    def validate_deployment(self):
        # type: (T_SELF) -> T_SELF
        iss = self.get_iss()
        client_id = self.get_client_id()
        deployment_id = self._get_deployment_id()
        tool_config = self._tool_config  # type: ToolConfAbstract

        # Find deployment.
        if tool_config.check_iss_has_one_client(iss):
            deployment = tool_config.find_deployment(iss, deployment_id)
        else:
            deployment = tool_config.find_deployment_by_params(iss, deployment_id, client_id)
        if not deployment:
            raise LtiException("Unable to find deployment")

        return self

    def validate_message(self):
        # type: (T_SELF) -> T_SELF
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

    def set_launch_data_storage(self, data_storage):
        data_storage.set_request(self._request)
        session_cookie_name = data_storage.get_session_cookie_name()
        if session_cookie_name:
            session_id = self._cookie_service.get_cookie(session_cookie_name)
            if session_id:
                data_storage.set_session_id(session_id)
            else:
                raise LtiException("Missing %s cookie" % session_cookie_name)
        self._session_service.set_data_storage(data_storage)
        return self

    def set_launch_data_lifetime(self, time_sec):
        # type: (T_SELF, int) -> T_SELF
        self._session_service.set_launch_data_lifetime(time_sec)
        return self

    def save_launch_data(self):
        # type: (T_SELF) -> T_SELF
        state_from_request = self._get_request_param('state')
        id_token_hash = self._get_id_token_hash()

        self._session_service.save_launch_data(self._launch_id, self._jwt['body'])
        self._session_service.set_state_valid(state_from_request, id_token_hash)
        return self

    def get_params_from_login(self):
        # type: () -> object
        state = self._get_request_param('state')
        return self._session_service.get_state_params(state)

    def check_jwt_body_is_empty(self):
        # type: () -> bool
        jwt_body = self._get_jwt_body()
        return not jwt_body

    def check_staff_access(self):
        # type: () -> bool
        jwt_body = self._get_jwt_body()
        return StaffRole(jwt_body).check()

    def check_student_access(self):
        # type: () -> bool
        jwt_body = self._get_jwt_body()
        return StudentRole(jwt_body).check()

    def check_teacher_access(self):
        # type: () -> bool
        jwt_body = self._get_jwt_body()
        return TeacherRole(jwt_body).check()

    def check_teaching_assistant_access(self):
        # type: () -> bool
        jwt_body = self._get_jwt_body()
        return TeachingAssistantRole(jwt_body).check()

    def check_designer_access(self):
        # type: () -> bool
        jwt_body = self._get_jwt_body()
        return DesignerRole(jwt_body).check()

    def check_observer_access(self):
        # type: () -> bool
        jwt_body = self._get_jwt_body()
        return ObserverRole(jwt_body).check()

    def check_transient(self):
        # type: () -> bool
        jwt_body = self._get_jwt_body()
        return TransientRole(jwt_body).check()
