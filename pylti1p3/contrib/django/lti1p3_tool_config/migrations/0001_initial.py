# mypy: ignore-errors
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LtiToolKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Key name', max_length=255, unique=True)),
                ('private_key', models.TextField(help_text="Tool's generated Private key. "
                                                           "Keep this value in secret")),
                ('public_key', models.TextField(blank=True, help_text="Tool's generated Public key", null=True)),
                ('public_jwk', models.TextField(blank=True, help_text="Tool's generated Public key (from the "
                                                                      "field above) presented as JWK.", null=True)),
            ],
            options={
                'verbose_name': 'lti 1.3 tool key',
                'verbose_name_plural': 'lti 1.3 tool keys',
                'db_table': 'lti1p3_tool_key',
            },
        ),
        migrations.CreateModel(
            name='LtiTool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('issuer', models.CharField(help_text="This will usually look something like 'http://example.com'. "
                                                      "Value provided by LTI 1.3 Platform", max_length=255)),
                ('client_id', models.CharField(help_text='Value provided by LTI 1.3 Platform', max_length=255)),
                ('use_by_default', models.BooleanField(default=False, help_text='This iss config will be used in case '
                                                                                'if client-id was not passed')),
                ('auth_login_url', models.CharField(help_text="The platform's OIDC login endpoint. "
                                                              "Value provided by LTI 1.3 Platform", max_length=1024,
                                                    validators=[django.core.validators.URLValidator()])),
                ('auth_token_url', models.CharField(help_text="The platform's service authorization endpoint. "
                                                              "Value provided by LTI 1.3 Platform", max_length=1024,
                                                    validators=[django.core.validators.URLValidator()])),
                ('auth_audience', models.CharField(blank=True, help_text="The platform's OAuth2 Audience (aud). "
                                                                         "Usually could be skipped", max_length=1024,
                                                   null=True)),
                ('key_set_url', models.CharField(blank=True, help_text="The platform's JWKS endpoint. "
                                                                       "Value provided by LTI 1.3 Platform",
                                                 max_length=1024, null=True,
                                                 validators=[django.core.validators.URLValidator()])),
                ('key_set', models.TextField(blank=True, help_text="In case if platform's JWKS endpoint somehow "
                                                                   "unavailable you may paste JWKS here. Value "
                                                                   "provided by LTI 1.3 Platform", null=True)),
                ('deployment_ids', models.TextField(help_text='List of Deployment IDs. Example: '
                                                              '["test-id-1", "test-id-2", ...] Each value '
                                                              'is provided by LTI 1.3 Platform. ')),
                ('tool_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lti_tools',
                                               to='lti1p3_tool_config.LtiToolKey')),
            ],
            options={
                'verbose_name': 'lti 1.3 tool',
                'verbose_name_plural': 'lti 1.3 tools',
                'db_table': 'lti1p3_tool',
                'unique_together': {('issuer', 'client_id')},
            },
        ),
    ]
