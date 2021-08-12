# mypy: ignore-errors
from django.contrib import admin

from .models import LtiTool, LtiToolKey


class LtiToolKeyAdmin(admin.ModelAdmin):
    """Admin for LTI Tool Key"""
    list_display = ('id', 'name')

    add_fieldsets = (
        (None, {'fields': ('name', 'private_key', 'public_key')}),
    )

    change_fieldsets = (
        (None, {'fields': ('name', 'private_key', 'public_key', 'public_jwk')}),
    )

    readonly_fields = ('public_jwk',)

    def get_form(self, request, obj=None, **kwargs):  # pylint: disable=arguments-differ
        help_texts = {'public_key_jwk_json': "Tool's generated Public key presented as JWK."}
        kwargs.update({'help_texts': help_texts})
        return super(LtiToolKeyAdmin, self).get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):  # pylint: disable=unused-argument
        if not obj:
            return self.add_fieldsets
        else:
            return self.change_fieldsets


class LtiToolAdmin(admin.ModelAdmin):
    """Admin for LTI Tool"""
    search_fields = ('title', 'issuer', 'client_id', 'auth_login_url', 'auth_token_url', 'key_set_url')
    list_display = ('id', 'title', 'is_active', 'issuer', 'client_id', 'deployment_ids')


admin.site.register(LtiToolKey, LtiToolKeyAdmin)
admin.site.register(LtiTool, LtiToolAdmin)
