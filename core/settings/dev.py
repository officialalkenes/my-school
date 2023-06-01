from base import *


DEBUG = True

DATABASES["default"].update(
    {
        "HOST": "localhost",
        "PORT": "5432",
        "OPTIONS": {
            "options": "-c search_path=dev",
        },
    }
)
