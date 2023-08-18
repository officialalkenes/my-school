from .base import *

# Example development-specific setting
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# DATABASE_ROUTERS = (
#     'django_tenants.routers.TenantSyncRouter',
# )

DATABASES["default"].update(
    DATABASES={
        "default": {
            "ENGINE": "django_tenants.postgresql_backend",
            # "ENGINE": "django.db.backends.postgresql",
            "NAME": config("NAME"),
            "USER": config("USER"),
            "PASSWORD": config("PASSWORD"),
        },
    },
)


# CELERY AND CELERY BEAT
CELERY_BROKER_URL = "redis://127.0.0.1:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Africa/Lagos"
