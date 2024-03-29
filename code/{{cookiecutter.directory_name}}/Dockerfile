# set base image (host OS)
FROM python:3.9-slim

{% if cookiecutter.dbDialect == "mssql" %}
# install FreeTDS and dependencies
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install tdsodbc -y \
 && apt-get install --reinstall build-essential -y

# populate "ocbcinst.ini"
RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

# install pyodbc (and, optionally, sqlalchemy)
RUN pip install --trusted-host pypi.python.org pyodbc==4.0.26 sqlalchemy==1.3.5
{% elif cookiecutter.dbDialect == "postgresql" %}
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
{% endif %}

# set the working directory in the container
WORKDIR /code

ENV FLASK_APP api
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

# copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "./entrypoint.sh"]
