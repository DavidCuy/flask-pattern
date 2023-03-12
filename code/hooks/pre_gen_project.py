import sys

if "{{ cookiecutter.dbDialect }}" == "sqlite":
    """{{ cookiecutter.update(
        {
            "_dbDriver": "sqlite",
            "_db_port": "",
            "_dbConn": "sqlite:///app.db"
        }
    )}}"""
elif "{{ cookiecutter.dbDialect }}" == "mysql":
    """{{ cookiecutter.update(
        {
            "_dbDriver": "pymysql",
            "_db_port": "3306",
            "_dbConn": "mysql+pymysql://{{ cookiecutter.db_user }}:{{ cookiecutter.db_pass }}@{{ cookiecutter.db_host }}/{{ cookiecutter.db_name }}"
        }
    )}}"""
elif "{{ cookiecutter.dbDialect }}" == "posgresql":
    """{{ cookiecutter.update(
        {
            "_dbDriver": "psycopg2",
            "_db_port": "5432",
            "_dbConn": "posgresql+psycopg2://{{ cookiecutter.db_user }}:{{ cookiecutter.db_pass }}@{{ cookiecutter.db_host }}/{{ cookiecutter.db_name }}"
        }
    )}}"""
elif "{{ cookiecutter.dbDialect }}" == "mssql":
    """{{ cookiecutter.update(
        {
            "_dbDriver": "pyodbc",
            "_db_port": "1433",
            "_dbConn": "mssql+pyodbc://{{ cookiecutter.db_user }}:{{ cookiecutter.db_pass }}@{{ cookiecutter.db_host }}/{{ cookiecutter.db_name }}"
        }
    )}}"""

sys.exit(0)
