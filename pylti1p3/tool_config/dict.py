from .abstract import ToolConfAbstract
from .mode import ToolConfMode
from ..registration import Registration
from ..deployment import Deployment


class ToolConfDict(ToolConfAbstract):
    _config = None
    _private_key = {}
    _public_key = {}

    def __init__(self, json_data):
        """
        json_data could be set in two formats:

        1. { "iss1": { ... "client_id: "client1" ... }, "iss2": { ... "client_id: "client2" ... } }
        In this case the library will work in the concept: one issuer ~ one client-id

        2. { "iss1": [ { ... "client_id: "client1" ... }, { ... "client_id: "client2" ... } ], ... }
        In this case the library will work in concept: one issuer ~ many client-ids

        The second type is preferred because it is more flexible.

        Example:
            {
                "iss1": [{
                        "default": True,
                        "client_id": "client_id1",
                        "auth_login_url": "auth_login_url1",
                        "auth_token_url": "auth_token_url1",
                        "key_set_url": "key_set_url1",
                        "key_set": None,
                        "private_key_file": "private.key",
                        "public_key_file": "public.key",
                        "deployment_ids": ["deployment_id1", "deployment_id2"]
                    }, {
                        "default": False,
                        "client_id": "client_id2",
                        "auth_login_url": "auth_login_url2",
                        "auth_token_url": "auth_token_url2",
                        "key_set_url": "key_set_url2",
                        "key_set": None,
                        "private_key_file": "private.key",
                        "public_key_file": "public.key",
                        "deployment_ids": ["deployment_id3", "deployment_id4"]
                    }],
                "iss2": [ .... ]
            }

        default (bool) - this iss config will be used in case if client-id is not passed
        client_id - this is the id received in the 'aud' during a launch
        auth_login_url - the platform's OIDC login endpoint
        auth_token_url - the platform's service authorization endpoint
        key_set_url - the platform's JWKS endpoint
        key_set - in case if platform's JWKS endpoint somehow unavailable you may paste JWKS here
        private_key_file - relative path to the tool's private key
        public_key_file - relative path to the tool's public key
        deployment_ids (list) - The deployment_id passed by the platform during launch
        """
        super(ToolConfDict, self).__init__()
        if not isinstance(json_data, dict):
            raise Exception("Invalid tool conf format. Must be dict")

        item_types = []
        for v in json_data.values():
            if isinstance(v, dict):
                item_types.append('dict')
            elif isinstance(v, list):
                item_types.append('list')
            else:
                raise Exception("Invalid tool conf format. Allowed types of elements: list or dict")

        item_types = list(set(item_types))
        if len(item_types) == 0:
            raise Exception("Invalid tool conf format. Config is empty")
        if len(item_types) > 1:
            raise Exception("Invalid tool conf format. All elements in config must have the same type")

        if item_types[0] == 'list':
            self.set_mode(ToolConfMode.ONE_ISSUER_MANY_CLIENT_IDS)
        self._config = json_data

    def _get_registration(self, iss, iss_conf):
        reg = Registration()
        reg.set_auth_login_url(iss_conf['auth_login_url'])\
            .set_auth_token_url(iss_conf['auth_token_url'])\
            .set_client_id(iss_conf['client_id'])\
            .set_key_set(iss_conf['key_set'])\
            .set_key_set_url(iss_conf['key_set_url'])\
            .set_issuer(iss)\
            .set_tool_private_key(self.get_private_key(iss, iss_conf['client_id']))
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
        iss_conf = self._get_iss_conf(iss)
        return self._get_registration(iss, iss_conf)

    def find_registration_by_params(self, iss, client_id, *args, **kwargs):
        iss_conf = self._get_iss_conf(iss, client_id)
        return self._get_registration(iss, iss_conf)

    def find_deployment(self, iss, deployment_id):
        iss_conf = self._get_iss_conf(iss)
        return self._get_deployment(iss_conf, deployment_id)

    def find_deployment_by_params(self, iss, deployment_id, client_id, *args, **kwargs):
        iss_conf = self._get_iss_conf(iss, client_id)
        return self._get_deployment(iss_conf, deployment_id)

    def set_public_key(self, iss, key_content, client_id=None):
        if client_id:
            if iss not in self._public_key:
                self._public_key[iss] = {}
            self._public_key[iss][client_id] = key_content
        else:
            self._public_key[iss] = key_content

    def get_public_key(self, iss, client_id=None):
        if iss in self._public_key:
            if isinstance(self._public_key[iss], dict):
                return self._public_key[iss].get(client_id)
            return self._public_key[iss]
        return None

    def set_private_key(self, iss, key_content, client_id=None):
        if client_id:
            if iss not in self._private_key:
                self._private_key[iss] = {}
            self._private_key[iss][client_id] = key_content
        else:
            self._private_key[iss] = key_content

    def get_private_key(self, iss, client_id=None):
        if isinstance(self._private_key[iss], dict):
            return self._private_key[iss].get(client_id)
        return self._private_key[iss]

    def _get_iss_conf(self, iss, client_id=None):
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
