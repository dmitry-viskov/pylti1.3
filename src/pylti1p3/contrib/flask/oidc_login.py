import typing as t
from flask import make_response, render_template  # type: ignore
from pylti1p3.oidc_login import OIDCLogin
from .cookie import FlaskCookieService
from .session import FlaskSessionService
from .redirect import FlaskRedirect


class FlaskOIDCLogin(OIDCLogin):
    cookie_check_template_name = "cookies_allowed_js_check.html"

    def __init__(
        self,
        request,
        tool_config,
        *,
        session_service: t.Optional[FlaskSessionService] = None,
        cookie_service: t.Optional[FlaskCookieService] = None,
        launch_data_storage=None,
    ):
        cookie_service = (
            cookie_service if cookie_service else FlaskCookieService(request)
        )
        session_service = (
            session_service if session_service else FlaskSessionService(request)
        )
        super().__init__(
            request=request,
            tool_config=tool_config,
            session_service=session_service,
            cookie_service=cookie_service,
            launch_data_storage=launch_data_storage,
        )

    def get_redirect(self, url):
        return FlaskRedirect(url, self._cookie_service)

    def get_response(self, html):
        return make_response(html)

    def get_cookie_check_template_name(self) -> str:
        return self.cookie_check_template_name

    def get_cookies_allowed_js_check(self):
        protocol, params = self.get_cookies_allowed_js_check_params()

        return render_template(
            self.get_cookie_check_template_name(),
            **{
                "protocol": protocol,
                "params": params,
                "main_text": self._cookies_unavailable_msg_main_text,
                "click_text": self._cookies_unavailable_msg_click_text,
                "loading_text": self._cookies_check_loading_text,
            },
        )
