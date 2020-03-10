from pylti1p3.oidc_login import OIDCLogin

from .redirect import FlaskRedirect


class FlaskOIDCLogin(OIDCLogin):
    def get_redirect(self, url):
        return FlaskRedirect(url, self._cookie_service)
