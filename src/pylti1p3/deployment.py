import typing as t


class Deployment:

    _deployment_id: t.Optional[str] = None

    def get_deployment_id(self) -> t.Optional[str]:
        return self._deployment_id

    def set_deployment_id(self, deployment_id: str) -> "Deployment":
        self._deployment_id = deployment_id
        return self
