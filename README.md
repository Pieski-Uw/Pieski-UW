# Pieski-UW
## Development database

A file inside `django/pieskiUW/secrets` folder called `postgresql.py` should be added for proper database connection.  
Example postgresql.py structure:
```py
SECRETS = {
    "HOST": "host",
    "PORT": 1234,
    "USER": "user",
    "PASSWORD": "password",
    "NAME": "database",
}
```
This file allows your django instance to connect to a postgresql database.

### Local database setup
A local database can be created with postgresql. I suggest following this tutorial for setup: ```https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04```
