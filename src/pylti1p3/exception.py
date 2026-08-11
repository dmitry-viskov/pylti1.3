import requests


class LtiException(Exception):
    pass


class OIDCException(Exception):
    pass


class LtiServiceException(LtiException):
    def __init__(self, message: str, response: requests.Response):
        msg = f"{message} HTTP response [{response.url}]: {response.status_code}"
        super().__init__(msg)
        self.response = response


class LtiJWTException(LtiException):
    """
    An error stemming from the JWT body of the message launch.
    """


class LtiMessageValidationException(LtiException):
    """
    An error encountered while validating an LTI launch message.
    """


class LtiInvalidNonceException(LtiMessageValidationException):
    """
    An error thrown when the nonce value in a message launch is not valid.
    """


class LtiKeyException(LtiException):
    """
    An error to do with keys for the OAuth process.
    """


class ToolConfException(Exception):
    """
    An error raised by a tool config.
    """


class SessionException(LtiException):
    """
    An error raised by a SessionService object.
    """


class LineItemException(LtiException):
    """
    An error raised by a LineItem object.
    """
