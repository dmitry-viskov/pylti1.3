from .abstract import ToolConfAbstract
from ..registration import Registration
from ..deployment import Deployment


class ToolConfDict(ToolConfAbstract):
    _config = None
    _private_key = {}

    def __init__(self, json_data):
        self._config = json_data

    def find_registration_by_issuer(self, iss):
        if iss not in self._config:
            raise Exception('iss %s not found in settings' % iss)

        iss_conf = self._config[iss]

        reg = Registration()
        return reg.set_auth_login_url(iss_conf['auth_login_url'])\
            .set_auth_token_url(iss_conf['auth_token_url'])\
            .set_client_id(iss_conf['client_id'])\
            .set_key_set(iss_conf['key_set'])\
            .set_key_set_url(iss_conf['key_set_url'])\
            .set_issuer(iss)\
            .set_tool_private_key(self.get_private_key(iss))

    def find_deployment(self, iss, deployment_id):
        if iss not in self._config:
            raise Exception('iss %s not found in settings' % iss)
        if deployment_id not in self._config[iss]['deployment_ids']:
            return None

        d = Deployment()
        return d.set_deployment_id(deployment_id)

    def set_private_key(self, iss, key_content):
        self._private_key[iss] = key_content

    def get_private_key(self, iss):
        return self._private_key[iss]
