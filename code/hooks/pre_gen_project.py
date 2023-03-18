import sys

db_dialect = "{{ cookiecutter.dbDialect }}"
print(f"--{db_dialect}--")
print(db_dialect == "mysql")

if db_dialect == "mysql":
    """{{ cookiecutter.update({
            "_dbDriver": "pymysql",
            "_db_port": "3306",
            "_dbConn": "mysql+pymysql://cookiecutter.db_user:cookiecutter.db_pass@cookiecutter.db_host/cookiecutter.db_name"
        }
    )}}"""
    sys.exit(0)
elif db_dialect == "posgresql":
    """{{ cookiecutter.update({
            "_dbDriver": "psycopg2",
            "_db_port": "5432",
            "_dbConn": "posgresql+psycopg2://cookiecutter.db_user:cookiecutter.db_pass@cookiecutter.db_host/cookiecutter.db_name"
        }
    )}}"""
    sys.exit(0)
elif db_dialect == "mssql":
    """{{ cookiecutter.update({
            "_dbDriver": "pyodbc",
            "_db_port": "1433",
            "_dbConn": "mssql+pyodbc://cookiecutter.db_user:cookiecutter.db_pass@cookiecutter.db_host/cookiecutter.db_name"
        }
    )}}"""
    sys.exit(0)
elif db_dialect == "sqlite":
    """{{ cookiecutter.update({
            "_dbDriver": "sqlite",
            "_db_port": "",
            "_dbConn": "sqlite:///app.db"
        }
    )}}"""
    sys.exit(0)
