# project/settings/staging.py

from .base import *

# Staging-specific settings
DEBUG = False

# Staging database configuration
DATABASES["default"].update(
    {
        "HOST": "staging.example.com",
        "PORT": "5432",
        "OPTIONS": {
            "options": "-c search_path=staging",
        },
    }
)

# Other staging-specific settings
# ...
