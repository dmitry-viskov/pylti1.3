"""
Dynamic registration flow.

Written with reference to:

* https://www.imsglobal.org/spec/lti-dr/v1p0
    - Learning Tools Interoperability (LTI) Dynamic Registration Specification
* https://gist.github.com/onemenzel/32d661649863a48efafce9e3fbbd6253 by Lukas Menzel / onamenzel
* https://moodlelti.theedtech.dev/dynreg/ - "LTI Advantage Automatic Registration" by Claude Vervoort
"""

from typing import Any, Dict

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import requests
from requests.exceptions import RequestException

from .exception import LtiException


def generate_key_pair(key_size: int = 4096) -> tuple[str, str]:
    """
    Generates an RSA key pair.

    :param key_size: key bits

    :returns: a dict with the keys "public" and "private", containing PEM-encoded RSA keys. \
        This is not returned as a tuple so that the user of this function never confuses them.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()

    private_key_str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()

    public_key_str = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()

    return (private_key_str, public_key_str)


class DynamicRegistration:
    """
    Controls the process of dynamic registration.
    """

    client_name = ""  # The name of the tool.
    description = ""  # A short plain-text description of the tool.

    response_types = ["id_token"]

    grant_types = ["implicit", "client_credentials"]

    def get_client_name(self) -> str:
        """
        Get the tool's name.
        """
        return self.client_name

    def get_response_types(self) -> list[str]:
        """
        Get the response types supported by the tool.

        Must include "id_token".
        """

        return self.response_types

    def get_grant_types(self):
        """
        Get the grant types supported by the tool.

        Must include "implicit" and "client_credentials".
        """

        return self.grant_types

    def get_initiate_login_uri(self) -> str:
        """
        Get the URI used by the platform to initiate the LTI launch.

        e.g. "https://example.com/login"
        """
        raise NotImplementedError

    def get_jwks_uri(self) -> str:
        """
        Get the URI to fetch the public JSON Web Key Set.

        e.g. "http://example.com/jwks"
        """
        raise NotImplementedError

    def get_redirect_uris(self) -> list[str]:
        """
        Get the tool's OIDC redirect URIs.
        """
        raise NotImplementedError

    def get_scopes(self) -> list[str]:
        """
        Get the list of scopes that the tool would like.

        Each entry should be a scope name following the naming conventions described at
        https://www.imsglobal.org/spec/security/v1p0/#h_scope-naming-conventions.

        e.g.::

            ['https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly']
        """
        return []

    def get_domain(self) -> str:
        """
        Get the domain that the tool runs on, including the port if necessary.

        e.g. "example.com:8000"
        """
        raise NotImplementedError

    def get_target_link_uri(self) -> str:
        """
        The actual end-point that should be executed at the end of the OpenID Connect authentication flow.

        e.g. "https://example.com/"
        """
        raise NotImplementedError

    def get_claims(self) -> list[str]:
        """
        A list of claims indicating which information this tool desires to be included in each idtoken.

        See https://www.imsglobal.org/spec/lti/v1p3#user-identity-claims

        ``'sub'`` is the only required claim.

        e.g.::

            ['iss', 'sub', 'name']
        """
        return [
            "sub",
        ]

    def get_messages(self) -> list[Dict[str, str]]:
        """
        A list of messages supported by this tool.

        Each should be a dict containing keys as described in the ``message`` table at
        https://www.imsglobal.org/spec/lti-dr/v1p0#tool-configuration-0.

        e.g.::

            [{
                'type': 'LtiDeepLinkingRequest',
                'target_link_uri': 'https://example.com/launch',
                'label': 'New tool link',
            }]
        """
        return []

    def get_description(self) -> str:
        """
        Get a short plain-text description of the tool.
        """
        return self.description

    def get_logo_uri(self) -> str:
        """
        Get the URI of the tool's logo image.

        e.g. "https://example.com/logo.png"
        """
        raise NotImplementedError

    def lti_registration_data(self) -> Dict[str, Any]:
        """
        Get the registration data object to send back to the platform.

        Must return an object matching the specification described at
        https://www.imsglobal.org/spec/lti-dr/v1p0#tool-configuration.
        """

        return {
            "response_types": self.get_response_types(),
            "application_type": "web",
            "client_name": self.get_client_name(),
            "initiate_login_uri": self.get_initiate_login_uri(),
            "grant_types": self.get_grant_types(),
            "jwks_uri": self.get_jwks_uri(),
            "token_endpoint_auth_method": "private_key_jwt",
            "redirect_uris": self.get_redirect_uris(),
            "scope": " ".join(self.get_scopes()),
            "https://purl.imsglobal.org/spec/lti-tool-configuration": {
                "domain": self.get_domain(),  # get_host includes the port.
                "target_link_uri": self.get_target_link_uri(),
                "claims": self.get_claims(),
                "messages": self.get_messages(),
                "description": self.get_description(),
            },
            "logo_uri": self.get_logo_uri(),
        }

    def get_openid_configuration_endpoint(self) -> str:
        """
        Get the URI of the public OpenID configuration endpoint.

        This is the ``openid_configuration`` parameter passed in the initial GET request from the platform.
        """
        raise NotImplementedError

    def get_registration_token(self) -> str:
        """
        Get the platform's registration token.

        This is the ``registration_token`` parameter passed in the initial GET request from the platform.
        """
        raise NotImplementedError

    def get_openid_configuration(self) -> Dict[str, Any]:
        openid_configuration_endpoint = self.get_openid_configuration_endpoint()

        with requests.Session() as session:
            resp = session.get(openid_configuration_endpoint)
            try:
                openid_configuration = resp.json()
            except RequestException as e:
                raise LtiException(
                    f"The OpenID configuration data is invalid: {e}"
                ) from e

        return openid_configuration

    def register(self) -> Dict[str, Any]:
        """
        Perform the tool registration.

        Returns the OpenID registration response as described.
        """

        openid_configuration_endpoint = self.get_openid_configuration_endpoint()
        registration_token = self.get_registration_token()

        if not openid_configuration_endpoint:
            raise LtiException("No OpenID configuration endpoint was specified.")

        openid_configuration = self.get_openid_configuration()

        with requests.Session() as session:

            assert (
                "registration_endpoint" in openid_configuration
            ), "The OpenID config does not have a registration endpoint."

            tool_provider_registration_endpoint = openid_configuration[
                "registration_endpoint"
            ]

            registration_data = self.lti_registration_data()

            headers = {"Accept": "application/json"}

            if registration_token is not None:
                headers["Authorization"] = "Bearer " + registration_token

            response = session.post(
                tool_provider_registration_endpoint,
                headers=headers,
                json=registration_data,
            )

            openid_registration = response.json()

        conf_spec = "https://purl.imsglobal.org/spec/lti-platform-configuration"
        assert (
            conf_spec in openid_configuration
        ), "The OpenID config is not an LTI platform configuration"

        tool_spec = "https://purl.imsglobal.org/spec/lti-tool-configuration"
        assert (
            tool_spec in openid_registration
        ), "The OpenID registration is not an LTI tool configuration"

        tool = self.complete_registration(openid_configuration, openid_registration)
        return tool

    def complete_registration(
        self, openid_configuration: Dict[str, Any], openid_registration: Dict[str, Any]
    ) -> Any:
        """
        Save the registration information.

        :param openid_configuration: the public configuration data returned by the platform.

        :param openid_registration: the object returned by the platform after registration, as described by
        https://www.imsglobal.org/spec/lti-dr/v1p0#tool-configuration-from-the-platform.

        :returns: an object representing the tool representation.
        """

        raise NotImplementedError

    def complete_html(self):
        """
        HTML for the final step of the process: it should make a JavaScript postMessage call to the platform,
        telling it that the registration process is complete.
        """

        return """
            <!doctype html>
            <html lang="en">
                <body>
                    <script>
                        (window.opener || window.parent).postMessage({subject:'org.imsglobal.lti.close'}, '*');
                    </script>
                    <p>The registration is now complete. You can close this window and return to the registered platform.</p>
                </body>
            </html>
        """  # noqa: E501
