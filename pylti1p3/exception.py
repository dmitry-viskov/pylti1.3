import requests


class LtiException(Exception):
    pass


class OIDCException(Exception):
    pass


class LtiServiceException(LtiException):
    def __init__(self, response: requests.Response):
        msg = f"HTTP response [{response.url}]: {str(response.status_code)} - {response.text}"
        super().__init__(msg)
        self.response = response
