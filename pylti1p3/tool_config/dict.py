import typing as t
import typing_extensions as te
from ..deployment import Deployment
from ..registration import Registration, TKeySet
from ..request import Request
from .abstract import ToolConfAbstract

TIssConf = te.TypedDict(
    "TIssConf",
    {
        "default": bool,
        "client_id": str,
        "auth_login_url": str,
        "auth_token_url": str,
        "auth_audience": t.Optional[str],
        "key_set_url": t.Optional[str],
        "key_set": t.Optional[TKeySet],
        "deployment_ids": t.List[str],
        "private_key_file": t.Optional[str],
        "public_key_file": t.Optional[str],
    },
    total=False,
)

TJsonData = t.Dict[str, t.Union[t.List[TIssConf], TIssConf]]


class ToolConfDict(ToolConfAbstract[Request]):
    _config = None
    _private_key_one_client: t.Dict[str, str]
    _public_key_one_client: t.Dict[str, str]
    _private_key_many_clients: t.Dict[str, t.Dict[str, str]]
    _public_key_many_clients: t.Dict[str, t.Dict[str, str]]

    def __init__(self, json_data: TJsonData):
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
        super().__init__()
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
                raise Exception(
                    "Invalid tool conf format. Allowed types of elements: list or dict"
                )

        self._config = json_data
        self._private_key_one_client = {}
        self._private_key_many_clients = {}
        self._public_key_one_client = {}
        self._public_key_many_clients = {}

    def _validate_iss_config_item(self, iss: str, iss_conf: TIssConf):
        if not isinstance(iss_conf, dict):
            raise Exception(
                f"Invalid configuration {iss} for the {str(iss_conf)} issuer. Must be dict"
            )
        required_keys = [
            "auth_login_url",
            "auth_token_url",
            "client_id",
            "deployment_ids",
        ]
        for key in required_keys:
            if key not in iss_conf:
                raise Exception(
                    f"Key '{key}' is missing in the {str(iss_conf)} config for the {iss} issuer"
                )
        if not isinstance(iss_conf["deployment_ids"], list):
            raise Exception(
                f"Invalid deployment_ids value in the {str(iss_conf)} config for the {iss} issuer. "
                f"Must be a list"
            )

    def _get_registration(self, iss: str, iss_conf: TIssConf) -> Registration:
        reg = Registration()
        reg.set_auth_login_url(iss_conf["auth_login_url"]).set_auth_token_url(
            iss_conf["auth_token_url"]
        ).set_client_id(iss_conf["client_id"]).set_key_set(
            iss_conf.get("key_set")
        ).set_key_set_url(
            iss_conf.get("key_set_url")
        ).set_issuer(
            iss
        ).set_tool_private_key(
            self.get_private_key(iss, iss_conf["client_id"])
        )
        auth_audience = iss_conf.get("auth_audience")
        if auth_audience:
            reg.set_auth_audience(auth_audience)
        public_key = self.get_public_key(iss, iss_conf["client_id"])
        if public_key:
            reg.set_tool_public_key(public_key)
        return reg

    def _get_deployment(self, iss_conf: TIssConf, deployment_id: str):
        if deployment_id not in iss_conf["deployment_ids"]:
            return None
        d = Deployment()
        return d.set_deployment_id(deployment_id)

    def find_registration_by_issuer(self, iss: str, *args, **kwargs):
        # pylint: disable=unused-argument
        iss_conf = self.get_iss_config(iss)
        return self._get_registration(iss, iss_conf)

    def find_registration_by_params(self, iss: str, client_id: str, *args, **kwargs):
        # pylint: disable=unused-argument
        iss_conf = self.get_iss_config(iss, client_id)
        return self._get_registration(iss, iss_conf)

    def find_deployment(self, iss: str, deployment_id: str):
        iss_conf = self.get_iss_config(iss)
        return self._get_deployment(iss_conf, deployment_id)

    def find_deployment_by_params(
        self, iss: str, deployment_id: str, client_id: str, *args, **kwargs
    ):
        # pylint: disable=unused-argument
        iss_conf = self.get_iss_config(iss, client_id)
        return self._get_deployment(iss_conf, deployment_id)

    def set_public_key(
        self, iss: str, key_content: str, client_id: t.Optional[str] = None
    ):
        if self.check_iss_has_many_clients(iss):
            if not client_id:
                raise Exception("Can't set public key: missing client_id")
            if iss not in self._public_key_many_clients:
                self._public_key_many_clients[iss] = {}
            self._public_key_many_clients[iss][client_id] = key_content
        else:
            self._public_key_one_client[iss] = key_content

    def get_public_key(self, iss: str, client_id: t.Optional[str] = None):
        if self.check_iss_has_many_clients(iss):
            if not client_id:
                raise Exception("Can't get public key: missing client_id")
            clients_dict = self._public_key_many_clients.get(iss, {})
            if not isinstance(clients_dict, dict):
                raise Exception("Invalid clients data")
            return clients_dict.get(client_id)
        return self._public_key_one_client.get(iss)

    def set_private_key(
        self, iss: str, key_content: str, client_id: t.Optional[str] = None
    ):
        if self.check_iss_has_many_clients(iss):
            if not client_id:
                raise Exception("Can't set private key: missing client_id")
            if iss not in self._private_key_many_clients:
                self._private_key_many_clients[iss] = {}
            self._private_key_many_clients[iss][client_id] = key_content  # type: ignore
        else:
            self._private_key_one_client[iss] = key_content

    def get_private_key(self, iss: str, client_id: t.Optional[str] = None):
        if self.check_iss_has_many_clients(iss):
            if not client_id:
                raise Exception("Can't get private key: missing client_id")
            clients_dict = self._private_key_many_clients.get(iss, {})
            if not isinstance(clients_dict, dict):
                raise Exception("Invalid clients data")
            return clients_dict.get(client_id)
        return self._private_key_one_client.get(iss)

    def get_iss_config(self, iss: str, client_id: t.Optional[str] = None):
        if not self._config:
            raise Exception("Config is not set")
        if iss not in self._config:
            raise Exception(f"iss {iss} not found in settings")
        config_iss = self._config[iss]

        if isinstance(config_iss, list):
            items_len = len(config_iss)
            for subitem in config_iss:
                # pylint: disable=too-many-boolean-expressions
                if (
                    (client_id and subitem["client_id"] == client_id)
                    or (not client_id and subitem.get("default", False))
                    or (not client_id and items_len == 1)
                ):
                    return subitem
            raise Exception(f"iss {iss} [client_id={client_id}] not found in settings")
        return config_iss

    def get_jwks(
        self, iss: t.Optional[str] = None, client_id: t.Optional[str] = None, **kwargs
    ):
        # pylint: disable=unused-argument
        if iss or client_id:
            return super().get_jwks(iss, client_id)

        public_keys = []
        for iss_item1 in self._public_key_one_client.values():
            if iss_item1 not in public_keys:
                public_keys.append(iss_item1)
        for iss_item2 in self._public_key_many_clients.values():
            for pub_key in iss_item2.values():
                if pub_key not in public_keys:
                    public_keys.append(pub_key)

        return {"keys": [Registration.get_jwk(k) for k in public_keys]}
