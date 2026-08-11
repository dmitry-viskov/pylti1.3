from django.conf import settings


def pytest_configure():
    settings.configure(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }
    )
