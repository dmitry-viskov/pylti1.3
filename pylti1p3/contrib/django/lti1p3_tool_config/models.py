# mypy: ignore-errors
import json

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from pylti1p3.registration import Registration


class LtiToolKey(models.Model):
    name = models.CharField(
        max_length=255, null=False, blank=False, unique=True, help_text=_("Key name")
    )
    private_key = models.TextField(
        null=False,
        blank=False,
        help_text=_("Tool's generated Private key. Keep this value in secret"),
    )
    public_key = models.TextField(
        null=True, blank=True, help_text=_("Tool's generated Public key")
    )
    public_jwk = models.TextField(
        null=True,
        blank=True,
        help_text=_(
            "Tool's generated Public key (from the field above) presented as JWK."
        ),
    )

    def save(
        self, *args, **kwargs
    ):  # pylint: disable=arguments-differ,signature-differs
        if self.public_key:
            public_jwk_dict = Registration.get_jwk(self.public_key)
            self.public_jwk = json.dumps(public_jwk_dict)
        else:
            self.public_key = None
            self.public_jwk = None
        super().save(*args, **kwargs)

    def __str__(self):
        # pylint: disable=no-member
        return f"<LtiToolKey id={self.id}, name={self.name}>"

    class Meta:
        db_table = "lti1p3_tool_key"
        verbose_name = "lti 1.3 tool key"
        verbose_name_plural = "lti 1.3 tool keys"


class LtiTool(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    issuer = models.CharField(
        max_length=255,
        help_text=_(
            "This will usually look something like 'http://example.com'. "
            "Value provided by LTI 1.3 Platform"
        ),
    )
    client_id = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text=_("Value provided by LTI 1.3 Platform"),
    )
    use_by_default = models.BooleanField(
        default=False,
        help_text=_("This iss config will be used in case if client-id was not passed"),
    )
    auth_login_url = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
        help_text=_(
            "The platform's OIDC login endpoint. Value provided by LTI 1.3 Platform"
        ),
        validators=[URLValidator()],
    )
    auth_token_url = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
        help_text=_(
            "The platform's service authorization "
            "endpoint. Value provided by "
            "LTI 1.3 Platform"
        ),
        validators=[URLValidator()],
    )
    auth_audience = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        help_text=_("The platform's OAuth2 Audience (aud). Usually could be skipped"),
    )
    key_set_url = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        help_text=_("The platform's JWKS endpoint. Value provided by LTI 1.3 Platform"),
        validators=[URLValidator()],
    )
    key_set = models.TextField(
        null=True,
        blank=True,
        help_text=_(
            "In case if platform's JWKS endpoint somehow "
            "unavailable you may paste JWKS here. "
            "Value provided by LTI 1.3 Platform"
        ),
    )
    tool_key = models.ForeignKey(
        LtiToolKey, on_delete=models.PROTECT, related_name="lti_tools"
    )
    deployment_ids = models.TextField(
        null=False,
        blank=False,
        help_text=_(
            "List of Deployment IDs. "
            'Example: ["test-id-1", "test-id-2", ...] '
            "Each value is provided by LTI 1.3 Platform. "
        ),
    )

    def clean(self):
        if not self.key_set_url and not self.key_set:
            raise ValidationError(
                {
                    "key_set_url": _(
                        'Even one of "key_set_url" or "key_set" should be set'
                    )
                }
            )

        if self.key_set:
            key_set_valid = False
            try:
                key_set_data = json.loads(self.key_set)
                if isinstance(key_set_data, dict):
                    key_set_valid = True
            except ValueError:
                pass
            if not key_set_valid:
                raise ValidationError({"key_set": _("Should be a dict")})

        deployment_ids_valid = False
        try:
            deployment_ids_data = json.loads(self.deployment_ids)
            if isinstance(deployment_ids_data, list):
                deployment_ids_valid = True
        except ValueError:
            pass
        if not deployment_ids_valid:
            raise ValidationError(
                {
                    "deployment_ids": _(
                        'Should be a list. Example: ["test-id-1", "test-id-2", ...]'
                    )
                }
            )

    def to_dict(self):
        data = {
            "issuer": self.issuer,
            "client_id": self.client_id,
            "auth_login_url": self.auth_login_url,
            "auth_token_url": self.auth_token_url,
            "auth_audience": self.auth_audience,
            "key_set_url": self.key_set_url,
            "key_set": json.loads(self.key_set) if self.key_set else None,
            "deployment_ids": json.loads(self.deployment_ids)
            if self.deployment_ids
            else [],
        }
        return data

    class Meta:
        unique_together = [
            ["issuer", "client_id"],
        ]
        db_table = "lti1p3_tool"
        verbose_name = "lti 1.3 tool"
        verbose_name_plural = "lti 1.3 tools"
