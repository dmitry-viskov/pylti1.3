import typing as t
from django.http import HttpResponse, HttpRequest  # type: ignore
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from pylti1p3.cookies_allowed_check import CookiesAllowedCheckPage
from pylti1p3.oidc_login import OIDCLogin

from .cookie import DjangoCookieService
from .redirect import DjangoRedirect
from .request import DjangoRequest
from .session import DjangoSessionService
from .lti1p3_tool_config import DjangoDbToolConf


class DjangoOIDCLogin(
    OIDCLogin[
        DjangoRequest,
        DjangoDbToolConf,
        DjangoSessionService,
        DjangoCookieService,
        HttpResponse,
    ]
):
    def __init__(
        self,
        request: HttpRequest,
        tool_config: DjangoDbToolConf,
        *,
        session_service: t.Optional[DjangoSessionService] = None,
        cookie_service: t.Optional[DjangoCookieService] = None,
        launch_data_storage=None,
    ):
        django_request = DjangoRequest(request)
        cookie_service = (
            cookie_service if cookie_service else DjangoCookieService(django_request)
        )
        session_service = (
            session_service if session_service else DjangoSessionService(django_request)
        )
        super().__init__(
            request=django_request,
            tool_config=tool_config,
            session_service=session_service,
            cookie_service=cookie_service,
            launch_data_storage=launch_data_storage,
        )

    def get_redirect(self, url):
        return DjangoRedirect(url, self._cookie_service)

    def get_response(self, html):
        return HttpResponse(html)

    def get_cookies_allowed_js_check(self) -> HttpResponse:
        protocol, params = self.get_cookies_allowed_js_check_params()

        try:
            request = self._request.request
            return render(
                request,
                "pylti1p3/cookies_allowed_js_check.html",
                {
                    "protocol": protocol,
                    "params": params,
                    "main_text": self._cookies_unavailable_msg_main_text,
                    "click_text": self._cookies_unavailable_msg_click_text,
                    "loading_text": self._cookies_check_loading_text,
                },
            )
        except TemplateDoesNotExist:
            html = CookiesAllowedCheckPage(
                params=params,
                protocol=protocol,
                main_text=self._cookies_unavailable_msg_main_text,
                click_text=self._cookies_unavailable_msg_click_text,
                loading_text=self._cookies_check_loading_text,
            ).get_html()
            return self.get_response(html)
