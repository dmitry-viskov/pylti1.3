class Deployment(object):

    _deployment_id = None

    def get_deployment_id(self):
        return self._deployment_id

    def set_deployment_id(self, deployment_id):
        self._deployment_id = deployment_id
        return self
