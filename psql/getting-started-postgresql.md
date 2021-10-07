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


# How to create user , password and make a new db.

Create the database (change database_name)
```
CREATE DATABASE database_name;
```
Create user (change my_username and my_password)
```
CREATE USER my_username WITH PASSWORD 'my_password';
```
Grant privileges on database to user
```
GRANT ALL PRIVILEGES ON DATABASE "database_name" to my_username;
```
