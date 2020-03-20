import typing as t

from ..deployment import Deployment
from ..registration import Registration
from ..request import Request
from .abstract import ToolConfAbstract

if t.TYPE_CHECKING:
    from ..message_launch import _LaunchData
    from typing_extensions import Literal
    from .abstract import FIND_REG_KWARGS


class ToolConfDict(ToolConfAbstract[Request[object]]):
    _config = None  # type: dict
    _private_key = {}  # type: t.Dict[str, str]

    def __init__(self, json_data):
        # type: (dict) -> None
        super(ToolConfDict, self).__init__()
        self._config = json_data

    def find_registration_by_issuer(self, iss, *args, **kwargs):  # pylint: disable=unused-argument
        # type: (str, *None, **FIND_REG_KWARGS) -> t.Optional[Registration]
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

    def find_deployment(self, iss, deployment_id, get_param):  # pylint: disable=unused-argument
        # type: (str, str, t.Callable[[str], object]) -> t.Optional[Deployment]
        if iss not in self._config:
            raise Exception('iss %s not found in settings' % iss)
        if deployment_id not in self._config[iss]['deployment_ids']:
            return None

        d = Deployment()
        return d.set_deployment_id(deployment_id)

    def set_private_key(self, iss, key_content):
        # type: (str, str) -> None
        self._private_key[iss] = key_content

    def get_private_key(self, iss):
        # type: (str) -> str
        return self._private_key[iss]
