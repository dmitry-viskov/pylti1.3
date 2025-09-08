from fastapi.responses import HTMLResponse, RedirectResponse

from pylti1p3.redirect import Redirect


class FastAPIRedirect(Redirect):
    _location = None
    _cookie_service = None

    def __init__(self, location, cookie_service=None):
        super().__init__()
        self._location = location
        self._cookie_service = cookie_service

    def do_redirect(self):
        return self._process_response(RedirectResponse(self._location, status_code=302))

    def do_js_redirect(self):
        return self._process_response(
            HTMLResponse(
                f'<script type="text/javascript">window.location="{self._location}";</script>'
            )
        )

    def set_redirect_url(self, location):
        self._location = location

    def get_redirect_url(self):
        return self._location

    def _process_response(self, response):
        if self._cookie_service:
            self._cookie_service.update_response(response)
        return response
