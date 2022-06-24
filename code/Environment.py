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

DB_DRIVER               = env("DB_DRIVER", "sqlite")
DB_CONNECTION_STRING    = env("DB_CONNECTION_STRING", "sqlite:///app.db")
