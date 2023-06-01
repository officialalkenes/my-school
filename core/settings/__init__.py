# project/settings/__init__.py

import os

# Import the appropriate settings file based on the current environment
if os.getenv("DJANGO_ENV") == "dev":
    from .dev import *
elif os.getenv("DJANGO_ENV") == "staging":
    from .staging import *
elif os.getenv("DJANGO_ENV") == "prod":
    from .prod import *
else:
    from .docker import *
