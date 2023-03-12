import sys
import json

db_dialect = "{{ cookiecutter.dbDialect }}"
db_user = "{{ cookiecutter.db_user }}"
db_pass = "{{ cookiecutter.db_pass }}"
db_host = "{{ cookiecutter.db_host }}"
db_name = "{{ cookiecutter.db_name }}"
db_driver = "sqlite"
db_port = ""

if db_dialect == "mysql":
    db_driver = "pymysql"
    db_port = "3306"
elif db_dialect == "posgresql":
    db_driver = "psycopg2"
    db_port = "5432"
elif db_dialect == "mssql":
    db_driver = "pyodbc"
    db_port = "1433"

db_conn = f"{db_driver}:///app.db" if db_dialect == "sqlite" else f"{db_dialect}+{db_driver}://{db_user}:{db_pass}@{db_host}/{db_name}"

"""{{ cookiecutter.update(
    {
        "_dbDriver": "{0}",
        "_db_port": "{1}",
        "_dbConn": "{2}"
    }
)}}""".format(db_driver, db_port, db_conn)

sys.exit(0)
