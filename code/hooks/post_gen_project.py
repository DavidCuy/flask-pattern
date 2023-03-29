import os
import sys

PROJECT_DIR = './' + '{{ cookiecutter.repository }}'

REMOVE_PATHS = [
    {% if cookiecutter.dbDialect != "mssql" %} PROJECT_DIR + '/odbcinst.ini', {% endif %}
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.unlink(path)

env_body = """APP_NAME="<APP NAME>"
APP_URL="<APP URL>"
APP_DESCRIPTION="<APP DESCRIPTION>"
ENVIRONMENT="<ENVIRONMENT>"

DB_USER="<DB USER>"
DB_PASSWORD="<DB PASSWORD>"
DB_HOST="<DB HOST>"
DB_SCHEMA="<DB SCHEMA>"
DB_DRIVER="<DB DRIVER>"
DB_PORT="<DB PORT>"
DB_CONNECTION_STRING="<DB CONNECTION STRING>"
"""

os.rename(PROJECT_DIR + '/.env.dist', PROJECT_DIR + '/.env')

with open(PROJECT_DIR + '/.env.dist', 'w+') as f:
    f.write(env_body)

