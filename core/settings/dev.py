from .base import *

# Example development-specific setting
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


DATABASES["default"].update(
    DATABASES={
        "default": {
            "ENGINE": "django_tenants.postgresql_backend",
            # "ENGINE": "django.db.backends.postgresql",
            "NAME": config("NAME"),
            "USER": config("USER"),
            "PASSWORD": config("PASSWORD"),
        }
    }
)
