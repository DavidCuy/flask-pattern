import Environment as env

config = {
    '{{cookiecutter._dbDriver}}': {
        'conn_string': env.DB_CONNECTION_STRING
    }
}