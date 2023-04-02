# Pieski-UW
## Development database
All database credentials are kept secret and stored as github secrets. All of them can be accessed by repository contributors.  
A file inside `secrets` folder called `postgresql.py` should be added for proper database connection.  
File structure:
```py
SECRETS = {
    "HOST": "host",
    "PORT": 1234,
    "USER": "user",
    "PASSWORD": "password",
    "NAME": "database",
}
```
### Local
A local database can be created with postgresql. I suggest following this tutorial for setup: ```https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04```

### Remote
A remote development database is available, all credentials ale stored in github secrets.