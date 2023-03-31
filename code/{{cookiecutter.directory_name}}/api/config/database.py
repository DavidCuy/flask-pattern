import Environment as env

config = {
    '{{ "pymysql" if cookiecutter.dbDialect == "mysql" else "psycopg2" if cookiecutter.dbDialect == "postgresql" else "mssql" cookiecutter.dbDialect == "mssql" else "sqlite" }}': {
        'conn_string': env.DB_CONNECTION_STRING
    }
}