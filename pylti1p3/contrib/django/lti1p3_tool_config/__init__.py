import json

from pylti1p3.deployment import Deployment
from pylti1p3.exception import LtiException
from pylti1p3.registration import Registration
from pylti1p3.tool_config.abstract import ToolConfAbstract


default_app_config = (
    "pylti1p3.contrib.django.lti1p3_tool_config.apps.PyLTI1p3ToolConfig"
)


class DjangoDbToolConf(ToolConfAbstract):
    _lti_tools = None
    _tools_cls = None
    _keys_cls = None

    def __init__(self):
        # pylint: disable=import-outside-toplevel
        from .models import LtiTool, LtiToolKey

        super().__init__()
        self._lti_tools = {}
        self._tools_cls = LtiTool
        self._keys_cls = LtiToolKey

    def get_lti_tool(self, iss, client_id):
        # pylint: disable=no-member
        lti_tool = (
            self._lti_tools.get(iss)
            if client_id is None
            else self._lti_tools.get(iss, {}).get(client_id)
        )
        if lti_tool:
            return lti_tool

        if client_id is None:
            lti_tool = (
                self._tools_cls.objects.filter(issuer=iss, is_active=True)
                .order_by("use_by_default")
                .first()
            )
        else:
            try:
                lti_tool = self._tools_cls.objects.get(
                    issuer=iss, client_id=client_id, is_active=True
                )
            except self._tools_cls.DoesNotExist:
                pass

        if lti_tool is None:
            raise LtiException(
                f"iss {iss} [client_id={client_id}] not found in settings"
            )

        if client_id is None:
            self._lti_tools[iss] = lti_tool
        else:
            if iss not in self._lti_tools:
                self._lti_tools[iss] = {}
            self._lti_tools[iss][client_id] = lti_tool

        return lti_tool

    def check_iss_has_one_client(self, iss):
        return False

    def check_iss_has_many_clients(self, iss):
        return True

    def find_registration_by_issuer(self, iss, *args, **kwargs):
        pass

    def find_registration_by_params(self, iss, client_id, *args, **kwargs):
        lti_tool = self.get_lti_tool(iss, client_id)
        auth_audience = lti_tool.auth_audience if lti_tool.auth_audience else None
        key_set = json.loads(lti_tool.key_set) if lti_tool.key_set else None
        key_set_url = lti_tool.key_set_url if lti_tool.key_set_url else None
        tool_public_key = (
            lti_tool.tool_key.public_key if lti_tool.tool_key.public_key else None
        )

        reg = Registration()
        reg.set_auth_login_url(lti_tool.auth_login_url).set_auth_token_url(
            lti_tool.auth_token_url
        ).set_auth_audience(auth_audience).set_client_id(
            lti_tool.client_id
        ).set_key_set(
            key_set
        ).set_key_set_url(
            key_set_url
        ).set_issuer(
            lti_tool.issuer
        ).set_tool_private_key(
            lti_tool.tool_key.private_key
        ).set_tool_public_key(
            tool_public_key
        )
        return reg

    def find_deployment(self, iss, deployment_id):
        pass

    def find_deployment_by_params(self, iss, deployment_id, client_id, *args, **kwargs):
        lti_tool = self.get_lti_tool(iss, client_id)
        deployment_ids = (
            json.loads(lti_tool.deployment_ids) if lti_tool.deployment_ids else []
        )
        if deployment_id not in deployment_ids:
            return None
        d = Deployment()
        return d.set_deployment_id(deployment_id)

    def get_jwks(self, iss=None, client_id=None, **kwargs):
        # pylint: disable=no-member
        search_kwargs = {}
        if iss:
            search_kwargs["lti_tools__issuer"] = iss
        if client_id:
            search_kwargs["lti_tools__client_id"] = client_id

        if search_kwargs:
            search_kwargs["lti_tools__is_active"] = True
            qs = self._keys_cls.objects.filter(**search_kwargs)
        else:
            qs = self._keys_cls.objects.all()

        jwks = []
        public_key_lst = []

        for key in qs:
            if key.public_key and key.public_key not in public_key_lst:
                if key.public_jwk:
                    jwks.append(json.loads(key.public_jwk))
                else:
                    jwks.append(Registration.get_jwk(key.public_key))
                public_key_lst.append(key.public_key)
        return {"keys": jwks}
