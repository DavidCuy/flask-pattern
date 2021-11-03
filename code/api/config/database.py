from Environment import env

DB_HOST     = env("DB_HOST", "localhost")
DB_USER     = env("DB_USER", "user")
DB_PWD      = env("DB_PWD", "secret")
DB_NAME     = env("DB_NAME", "dbname")
DB_PORT     = env("DB_PORT", 1443)
DB_DRIVER   = env("DB_DRIVER", "sql+driver")