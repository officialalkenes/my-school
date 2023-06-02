from .base import *

# Example development-specific setting
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


DATABASES["default"].update(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
)
