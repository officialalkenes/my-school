from decouple import config

# Import the appropriate settings file based on the current environment
ENVIRONMENT = config("ENVIRONMENT")

if ENVIRONMENT == "dev":
    from .dev import *
elif ENVIRONMENT == "prod":
    from .prod import *
elif ENVIRONMENT == "staging":
    from .staging import *
else:
    raise ValueError("Invalid environment specified.")
