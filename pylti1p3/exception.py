import typing as t

if t.TYPE_CHECKING:
    # pylint: disable=unused-import
    import requests


class LtiException(Exception):
    pass


class OIDCException(Exception):
    pass


class LtiServiceException(LtiException):
    def __init__(self, response):
        # type: (requests.Response) -> None
        msg = 'HTTP response [%s]: %s - %s' % (
            response.url,
            str(response.status_code),
            response.text,
        )
        super(LtiServiceException, self).__init__(msg)
        self.response = response
