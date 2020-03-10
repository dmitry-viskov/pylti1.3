from flask import make_response, redirect
from werkzeug.wrappers import Response

from pylti1p3.redirect import Redirect


class FlaskRedirect(Redirect):
    _location = None
    _cookie_service = None

    def __init__(self, location: str, cookie_service=None):
        self._location = location
        self._cookie_service = cookie_service

    def do_redirect(self) -> Response:
        return self._process_response(redirect(self._location))

    def do_js_redirect(self) -> Response:
        return self._process_response(
            make_response('<script type="text/javascript">window.location={};'
                          '</script>'.format(self._location))
        )

    def set_redirect_url(self, location: str):
        self._location = location

    def get_redirect_url(self) -> str:
        return self._location

    def _process_response(self, response: Response) -> Response:
        if self._cookie_service:
            self._cookie_service.update_response(response)
        return response
