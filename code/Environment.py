import os
from typing import Any
from dotenv import load_dotenv

load_dotenv('.env')

def env(env_key: str, default_value: Any) -> Any:
    """ Parsea el valor de una variable de entorno a una variable utilizable para python

    Args:
        env_key (str): Nombre de la variable de entorno de
        default_value (Any): Valor por default de la variable de entorno

    Returns:
        Any: Valor designado de la variable de entorno o en su defecto la default
    """
    if env_key in os.environ:
        if os.environ[env_key].isdecimal():
            return int(os.environ[env_key])
        elif str(os.environ[env_key]).lower() == "true" or str(os.environ[env_key]).lower() == "true":
            return str(os.environ[env_key]).lower() == "true"
        else:
            return os.environ[env_key]
    else:
        return default_value

APP_NAME    = env("APP_NAME", "Flask app")
APP_URL     = env("APP_URL", "http://localhost")

DB_HOST     = env("DB_HOST", "localhost")
DB_USER     = env("DB_USER", "user")
DB_PWD      = env("DB_PWD", "secret")
DB_NAME     = env("DB_NAME", "dbname")
DB_PORT     = env("DB_PORT", 1443)
DB_ENGINE   = env("DB_ENGINE", "sql+engine")
DB_DRIVER   = env("DB_DRIVER", "sql+driver")

AWS_ACCESS_KEY      = env("AWS_ACCESS_KEY", "access_key")
AWS_SECRET_KEY      = env("AWS_SECRET_KEY", "secret_key")
BUCKET_NAME         = env("BUCKET_NAME", "bucket_name")
