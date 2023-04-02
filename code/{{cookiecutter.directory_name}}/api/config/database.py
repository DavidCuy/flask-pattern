import Environment as env

config = {
    '{{cookiecutter._driver}}': {
        'conn_string': env.DB_CONNECTION_STRING
    }
}