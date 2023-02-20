from   asgiref.sync import sync_to_async
from   django.urls import reverse_lazy
from   django.templatetags.static import static
import json
from   .models import LtiTool, LtiToolKey
from   pylti1p3.dynamic_registration import DynamicRegistration, generate_key_pair
from   typing import Any, Dict

class DjangoDynamicRegistration(DynamicRegistration):

    initiate_login_url = reverse_lazy('lti:login')

    jwks_url = reverse_lazy('lti:jwks')

    launch_url = reverse_lazy('lti:launch')

    # The path of the tool's logo image, under ``STATIC_ROOT``.
    logo_file = 'lti/logo.png'  

    def __init__(self, request):
        super().__init__()

        self.request = request

    async def get_issuer_keys(self, issuer_name : str):
        get_or_create_key = sync_to_async(LtiToolKey.objects.get_or_create)
        key_obj, created = await get_or_create_key(name=issuer_name)
        if created:
            private_key, public_key = await generate_key_pair()
            key_obj.private_key = private_key
            key_obj.public_key = public_key
            await sync_to_async(key_obj.save)()
        return key_obj

    def get_initiate_login_uri(self) -> str:
        return self.request.build_absolute_uri(str(self.initiate_login_url))

    def get_jwks_uri(self) -> str:
        return self.request.build_absolute_uri(str(self.jwks_url))

    def get_redirect_uris(self) -> list[str]:
        return [self.get_target_link_uri()]

    def get_domain(self) -> str:
        return self.request.get_host()

    def get_target_link_uri(self) -> str:
        return self.request.build_absolute_uri(self.launch_url)

    def get_logo_uri(self) -> str:
        return self.request.build_absolute_uri(static(self.logo_file))

    def get_openid_configuration_endpoint(self):
        return self.request.GET.get('openid_configuration')

    def get_registration_token(self):
        return self.request.GET.get('registration_token')

    def get_platform_name(self, openid_configuration: Dict[str, Any]) -> str:
        """
            Get the name of the platform this tool is registering with.
        """
        return openid_configuration.get("https://purl.imsglobal.org/spec/lti-platform-configuration",{}).get("product_family_code",'')

    async def complete_registration(self, openid_configuration: Dict[str, Any], openid_registration: Dict[str, Any]):
        title = self.get_platform_name(openid_configuration)

        tool_key = await self.get_issuer_keys(openid_configuration['issuer'])

        tool_spec = "https://purl.imsglobal.org/spec/lti-tool-configuration"
        deployment_ids = [openid_registration[tool_spec]['deployment_id']]

        platform_config, created = await LtiTool.objects.aupdate_or_create(
            issuer=openid_configuration['issuer'],
            client_id=openid_registration['client_id'],
            defaults = {
                'title': title,
                'auth_login_url': openid_configuration['authorization_endpoint'],
                'auth_token_url': openid_configuration['token_endpoint'],
                'auth_audience': openid_configuration['token_endpoint'],
                'key_set_url': openid_configuration['jwks_uri'],
                'tool_key': tool_key,
                'deployment_ids': json.dumps(deployment_ids),
            }
        )

        await sync_to_async(platform_config.save)() # type: ignore
        return platform_config

    async def keys_for_issuer(issuer_name: str) -> LtiToolKey:
        """
            Get the public and private keys for a given issuer.

            If they don't exist yet, then create them.
        """
        get_or_create_key = sync_to_async(LtiToolKey.objects.get_or_create)
        key_obj, created = await get_or_create_key(name=issuer_name)
        if created:
            key_pair = await generate_key_pair()
            key_obj.private_key = key_pair['private']
            key_obj.public_key = key_pair['public']
            await sync_to_async(key_obj.save)()
        return key_obj

