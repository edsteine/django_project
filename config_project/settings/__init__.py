import environ  # type: ignore

env_variables = environ.Env()
environ.Env.read_env(".env")

ENVIRONMENT = env_variables("DJANGO_ENVIRONMENT")  # Default to 'dev' if not set
if ENVIRONMENT == "prod":
    from .prod_config import *  # noqa: F403
else:
    from .dev_config import *  # noqa: F403
