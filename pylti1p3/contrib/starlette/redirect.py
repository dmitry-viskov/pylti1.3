from typing import Optional

from pylti1p3.redirect import Redirect
from starlette.responses import RedirectResponse, HTMLResponse, Response

from .cookie import StarletteCookieService


class StarletteRedirect(Redirect):

    def __init__(self, location, cookie_service: Optional[StarletteCookieService] = None):
        super().__init__()
        self._location = location
        self._cookie_service = cookie_service

    def do_redirect(self):
        response = RedirectResponse(url=self._location)
        self._process_response(response)
        return response

    def do_js_redirect(self):
        return self._process_response(
            HTMLResponse(f'<script type="text/javascript">window.location="{self._location}";</script>')
        )

    def set_redirect_url(self, location):
        self._location = location

    def get_redirect_url(self):
        return self._location

    def _process_response(self, response: Response):
        if self._cookie_service:
            self._cookie_service.update_response(response)
        return response
