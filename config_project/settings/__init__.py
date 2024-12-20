from environ import Env

# from environ import Env  # type: ignore[import-untyped]

env_variables = Env()
Env.read_env(".env")
# environ.Env.read_env()

ENVIRONMENT = env_variables("DJANGO_ENVIRONMENT")  # Default to 'dev' if not set
if ENVIRONMENT == "prod":
    from .prod_config import *  # noqa: F403
else:
    from .dev_config import *  # noqa: F403
