from ..exception import LtiException
from .abstract import MessageValidatorAbstract


class ResourceMessageValidator(MessageValidatorAbstract):

    def validate(self, jwt_body):
        self.run_common_validators(jwt_body)

        id_val = jwt_body.get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {}).get('id')
        if not id_val:
            raise LtiException('Missing Resource Link Id')

        return True

    def can_validate(self, jwt_body):
        return jwt_body.get('https://purl.imsglobal.org/spec/lti/claim/message_type') == 'LtiResourceLinkRequest'
