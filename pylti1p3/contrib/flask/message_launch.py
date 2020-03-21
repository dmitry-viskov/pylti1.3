from pylti1p3.message_launch import MessageLaunch


class FlaskMessageLaunch(MessageLaunch):
    def _get_request_param(self, key):
        return self._request.get_param(key)
