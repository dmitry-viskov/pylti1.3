import json
import os

from pylti1p3.tool_config import ToolConfAbstract
from pylti1p3.registration import Registration
from pylti1p3.deployment import Deployment


class ToolConf(ToolConfAbstract):
    _config = None
    _configs_dir = None

    def __init__(self, config_file):
        if not os.path.isfile(config_file):
            raise Exception("LTI tool config not found: " + config_file)
        self._configs_dir = os.path.dirname(config_file)
        with open(config_file, 'r') as f:
            self._config = json.loads(f.read())

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
            .set_tool_private_key(self._get_private_key(iss_conf['private_key_file']))

    def find_deployment(self, iss, deployment_id):
        if iss not in self._config:
            raise Exception('iss %s not found in settings' % iss)
        if deployment_id not in self._config[iss]['deployment']:
            raise Exception('deployment %s not found in the iss settings' % deployment_id)

        d = Deployment()
        return d.set_deployment_id(deployment_id)

    def _get_private_key(self, private_key_file):
        if not private_key_file.startswith('/'):
            private_key_file = self._configs_dir + '/' + private_key_file
        with open(private_key_file, 'r') as f:
            return f.read()
