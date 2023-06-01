from .base import *

# Example production-specific setting
ALLOWED_HOSTS = ["example.com"]

# Production database configuration
DATABASES["default"].update(
    {
        "HOST": "production.example.com",
        "PORT": "5432",
        "OPTIONS": {
            "options": "-c search_path=production",
        },
    }
)
