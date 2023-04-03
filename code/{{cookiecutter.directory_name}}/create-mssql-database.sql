IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{{ cookiecutter.db_name }}')
BEGIN
  CREATE DATABASE {{ cookiecutter.db_name }};
END;
GO