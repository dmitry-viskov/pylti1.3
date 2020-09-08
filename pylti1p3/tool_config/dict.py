import typing as t

from ..deployment import Deployment
from ..registration import Registration
from ..request import Request
from .abstract import ToolConfAbstract

if t.TYPE_CHECKING:
    from ..message_launch import _LaunchData
    from typing_extensions import Literal
    from .abstract import FIND_REG_KWARGS


class ToolConfDict(ToolConfAbstract[Request]):
    _config = None
    _private_key = None  # type: t.Optional[t.Mapping[str, str]]
    _public_key = None  # type: t.Optional[t.Mapping[str, str]]

    def __init__(self, json_data):
        # type: (dict) -> None
        """
        json_data is a dict where each key is issuer and value is issuer's configuration.
        Configuration could be set in two formats:

        1. { ... "iss": { ... "client_id: "client" ... }, ... }
        In this case the library will work in the concept: one issuer ~ one client-id

        2. { ... "iss": [ { ... "client_id: "client1" ... }, { ... "client_id: "client2" ... } ], ... }
        In this case the library will work in concept: one issuer ~ many client-ids

        Example:
            {
                "iss1": [{
                        "default": True,
                        "client_id": "client_id1",
                        "auth_login_url": "auth_login_url1",
                        "auth_token_url": "auth_token_url1",
                        "auth_audience": None,
                        "key_set_url": "key_set_url1",
                        "key_set": None,
                        "deployment_ids": ["deployment_id1", "deployment_id2"]
                    }, {
                        "default": False,
                        "client_id": "client_id2",
                        "auth_login_url": "auth_login_url2",
                        "auth_token_url": "auth_token_url2",
                        "auth_audience": None,
                        "key_set_url": "key_set_url2",
                        "key_set": None,
                        "deployment_ids": ["deployment_id3", "deployment_id4"]
                    }],
                "iss2": [ .... ]
            }

        default (bool) - this iss config will be used in case if client-id was not passed on the login step
        client_id - this is the id received in the 'aud' during a launch
        auth_login_url - the platform's OIDC login endpoint
        auth_token_url - the platform's service authorization endpoint
        auth_audience - the platform's OAuth2 Audience (aud). Is used to get platform's access token,
                        Usually the same as "auth_token_url" but in the common case could be a different url
        key_set_url - the platform's JWKS endpoint
        key_set - in case if platform's JWKS endpoint somehow unavailable you may paste JWKS here
        deployment_ids (list) - The deployment_id passed by the platform during launch
        """
        super(ToolConfDict, self).__init__()
        if not isinstance(json_data, dict):
            raise Exception("Invalid tool conf format. Must be dict")

        for iss, iss_conf in json_data.items():
            if isinstance(iss_conf, dict):
                self.set_iss_has_one_client(iss)
                self._validate_iss_config_item(iss, iss_conf)
            elif isinstance(iss_conf, list):
                self.set_iss_has_many_clients(iss)
                for v in iss_conf:
                    self._validate_iss_config_item(iss, v)
            else:
                raise Exception("Invalid tool conf format. Allowed types of elements: list or dict")

        self._config = json_data
        self._private_key = {}
        self._public_key = {}

    def _validate_iss_config_item(self, iss, iss_config_item):
        # type: (str, t.Any) -> None
        if not isinstance(iss_config_item, dict):
            raise Exception("Invalid configuration %s for the %s issuer. Must be dict" % (iss, str(iss_config_item)))
        required_keys = ['auth_login_url', 'auth_token_url', 'client_id', 'deployment_ids']
        for key in required_keys:
            if key not in iss_config_item:
                raise Exception("Key '%s' is missing in the %s config for the %s issuer"
                                % (key, str(iss_config_item), iss))
        if not isinstance(iss_config_item['deployment_ids'], list):
            raise Exception("Invalid deployment_ids value in the %s config for the %s issuer. Must be a list"
                            % (str(iss_config_item), iss))

    def _get_registration(self, iss, iss_conf):
        # type: (str, t.Any) -> Registration
        reg = Registration()
        reg.set_auth_login_url(iss_conf['auth_login_url'])\
            .set_auth_token_url(iss_conf['auth_token_url'])\
            .set_client_id(iss_conf['client_id'])\
            .set_key_set(iss_conf.get('key_set'))\
            .set_key_set_url(iss_conf.get('key_set_url'))\
            .set_issuer(iss)\
            .set_tool_private_key(self.get_private_key(iss, iss_conf['client_id']))
        auth_audience = iss_conf.get('auth_audience')
        if auth_audience:
            reg.set_auth_audience(auth_audience)
        public_key = self.get_public_key(iss, iss_conf['client_id'])
        if public_key:
            reg.set_tool_public_key(public_key)
        return reg

    def _get_deployment(self, iss_conf, deployment_id):
        if deployment_id not in iss_conf['deployment_ids']:
            return None
        d = Deployment()
        return d.set_deployment_id(deployment_id)

    def find_registration_by_issuer(self, iss, *args, **kwargs):
        # pylint: disable=unused-argument
        iss_conf = self.get_iss_config(iss)
        return self._get_registration(iss, iss_conf)

    def find_registration_by_params(self, iss, client_id, *args, **kwargs):
        # pylint: disable=unused-argument
        iss_conf = self.get_iss_config(iss, client_id)
        return self._get_registration(iss, iss_conf)

    def find_deployment(self, iss, deployment_id):
        iss_conf = self.get_iss_config(iss)
        return self._get_deployment(iss_conf, deployment_id)

    def find_deployment_by_params(self, iss, deployment_id, client_id, *args, **kwargs):
        # pylint: disable=unused-argument
        iss_conf = self.get_iss_config(iss, client_id)
        return self._get_deployment(iss_conf, deployment_id)

    def set_public_key(self, iss, key_content, client_id=None):
        if self.check_iss_has_many_clients(iss):
            if not client_id:
                raise Exception("Can't set public key: missing client_id")
            if iss not in self._public_key:
                self._public_key[iss] = {}
            self._public_key[iss][client_id] = key_content
        else:
            self._public_key[iss] = key_content

    def get_public_key(self, iss, client_id=None):
        if self.check_iss_has_many_clients(iss):
            if not client_id:
                raise Exception("Can't get public key: missing client_id")
            return self._public_key.get(iss, {}).get(client_id)
        else:
            return self._public_key.get(iss)

    def set_private_key(self, iss, key_content, client_id=None):
        if self.check_iss_has_many_clients(iss):
            if not client_id:
                raise Exception("Can't set private key: missing client_id")
            if iss not in self._private_key:
                self._private_key[iss] = {}
            self._private_key[iss][client_id] = key_content
        else:
            self._private_key[iss] = key_content

    def get_private_key(self, iss, client_id=None):
        if self.check_iss_has_many_clients(iss):
            if not client_id:
                raise Exception("Can't get private key: missing client_id")
            return self._private_key.get(iss, {}).get(client_id)
        else:
            return self._private_key.get(iss)

    def get_iss_config(self, iss, client_id=None):
        if iss not in self._config:
            raise Exception('iss %s not found in settings' % iss)

        if isinstance(self._config[iss], list):
            items_len = len(self._config[iss])
            for subitem in self._config[iss]:
                if (client_id and subitem['client_id'] == client_id)\
                        or (not client_id and subitem.get('default', False))\
                        or (not client_id and items_len == 1):
                    return subitem
            raise Exception('iss %s [client_id=%s] not found in settings' % (iss, client_id))
        return self._config[iss]

    def get_jwks(self, iss=None, client_id=None, **kwargs):
        # pylint: disable=unused-argument
        if iss or client_id:
            return super(ToolConfDict, self).get_jwks(iss, client_id)

        public_keys = []
        for iss_item in self._public_key.values():
            if isinstance(iss_item, dict):
                for pub_key in iss_item.values():
                    if pub_key not in public_keys:
                        public_keys.append(pub_key)
            else:
                if iss_item not in public_keys:
                    public_keys.append(iss_item)
        return {
            'keys': [Registration.get_jwk(k) for k in public_keys]
        }
