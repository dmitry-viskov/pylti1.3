from ..exception import LtiException
from .abstract import MessageValidatorAbstract


class DeepLinkMessageValidator(MessageValidatorAbstract):

    def validate(self, jwt_body):
        self.run_common_validators(jwt_body)

        if not jwt_body.get('https://purl.imsglobal.org/spec/lti-dl/claim/deep_linking_settings'):
            raise LtiException('Missing Deep Linking Settings')

        deep_link_settings = jwt_body.get('https://purl.imsglobal.org/spec/lti-dl/claim/deep_linking_settings')
        if not deep_link_settings:
            raise LtiException('Missing Deep Linking Return URL')

        accept_types = deep_link_settings.get('accept_types')

        if not isinstance(accept_types, list) or 'ltiResourceLink' not in accept_types:
            raise LtiException('Must support resource link placement types')

        if not deep_link_settings.get('accept_presentation_document_targets'):
            raise LtiException('Must support a presentation type')

        return True

    def can_validate(self, jwt_body):
        return jwt_body.get('https://purl.imsglobal.org/spec/lti/claim/message_type') == 'LtiDeepLinkingRequest'
