# How to create new database in postgresql?
```
create database <db-name>;
```

# Create admin user in postgresql
```
create user <user-name> with password '<your password>';
alter user <user-name> with superuser;
```

# How to take the postgresql dump?
```
pg_dump -h <host> -U <user> -d <database-name> > <path-where-we-want-to-store>/dump/sql
```

# How to restore the database? - if dump extension is `.sql`.
```
psql -h <host> -U <user> -d <database-name> > -f <path-where-we-want-to-store>/dump/sql
```
