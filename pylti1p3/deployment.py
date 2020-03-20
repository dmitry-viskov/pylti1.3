import typing as t

if t.TYPE_CHECKING:
    T_SELF = t.TypeVar('T_SELF', bound='Deployment')


class Deployment(object):

    _deployment_id = None  # type: t.Optional[str]

    def get_deployment_id(self):
        # type: () -> t.Optional[str]
        return self._deployment_id

    def set_deployment_id(self, deployment_id):
        # type: (T_SELF, str) -> T_SELF
        self._deployment_id = deployment_id
        return self
