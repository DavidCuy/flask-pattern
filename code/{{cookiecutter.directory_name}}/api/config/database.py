import Environment as env

config = {
    '{{cookiecutter.dbDialect == "mysql" ? "pymysql" : cookiecutter.dbDialect == "postgresql" ? "psycopg2" : cookiecutter.dbDialect == "mssql" ? "pyodbc" : "sqlite" }}': {
        'conn_string': env.DB_CONNECTION_STRING
    }
}