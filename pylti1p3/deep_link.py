import time
import uuid
import jwt


class DeepLink(object):
    _registration = None
    _deployment_id = None
    _deep_link_settings = None

    def __init__(self, registration, deployment_id, deep_link_settings):
        self._registration = registration
        self._deployment_id = deployment_id
        self._deep_link_settings = deep_link_settings

    def get_response_jwt(self, resources):
        message_jwt = {
            'iss': self._registration.get_client_id(),
            'aud': [self._registration.get_issuer()],
            'exp': int(time.time()) + 600,
            'iat': int(time.time()),
            'nonce': 'nonce-' + str(uuid.uuid4()),
            'https://purl.imsglobal.org/spec/lti/claim/deployment_id': self._deployment_id,
            'https://purl.imsglobal.org/spec/lti/claim/message_type': 'LtiDeepLinkingResponse',
            'https://purl.imsglobal.org/spec/lti/claim/version': '1.3.0',
            'https://purl.imsglobal.org/spec/lti-dl/claim/content_items': [r.to_dict() for r in resources],
            'https://purl.imsglobal.org/spec/lti-dl/claim/data': self._deep_link_settings['data']
        }
        return jwt.encode(message_jwt, self._registration.get_tool_private_key(), algorithm='RS256')

    def output_response_form(self, resources):
        jwt_val = self.get_response_jwt(resources)
        html = '<form id="lti13_deep_link_auto_submit" action="%s" method="POST">' \
               '<input type="hidden" name="JWT" value="%s" /></form>' \
               '<script type="text/javascript">document.getElementById(\'lti13_deep_link_auto_submit\').submit();' \
               '</script>' % (self._deep_link_settings['deep_link_return_url'], jwt_val)
        return html
