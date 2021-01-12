# Setup django

- Create `local_settings.py` file into Django project where settings.py is there.
- Add the.

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "<DBNAME>",
        "USER": "<DB-USERNAME>",
        "PASSWORD": "<DB-PASSWORD>",
        "HOST": "localhost",
        "PORT": "",
    }
}
```
- Create superuser in Postgresql with [link](https://github.com/hitul007/shortcuts/blob/master/psql/getting-started-psql.md#how-to-restore-the-database---if-dump-extension-is-sql).
- Restore the dump with the commands specified in link, Create superuser in Postgresql with [link](https://github.com/hitul007/shortcuts/blob/master/psql/getting-started-psql.md#how-to-restore-the-database---if-dump-extension-is-sql).
