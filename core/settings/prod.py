# project/settings/production.py

from .base import *

# Production-specific settings
DEBUG = config("DEBUG", cast=bool)

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

# Other production-specific settings
# ...
