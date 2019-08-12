from abc import ABCMeta, abstractmethod
from ..exception import LtiException


class MessageValidatorAbstract(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate(self, jwt_body):
        raise NotImplementedError

    @abstractmethod
    def can_validate(self, jwt_body):
        raise NotImplementedError

    def run_common_validators(self, jwt_body):
        if not jwt_body.get('sub'):
            raise LtiException('Must have a user (sub)')

        if jwt_body.get('https://purl.imsglobal.org/spec/lti/claim/version') != '1.3.0':
            raise LtiException('Incorrect version, expected 1.3.0')

        if not jwt_body.get('https://purl.imsglobal.org/spec/lti/claim/roles'):
            raise LtiException('Missing Roles Claim')
