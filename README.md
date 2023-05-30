# Pieski-UW
![Uptime Kuma](https://kuma.arturkamieniecki.pl//api/badge/1/uptime/24?label=Uptime%20Kuma)
## Database uptime
Database uptime can be checked at this address:  
[https://kuma.arturkamieniecki.pl/status/pieskiuw](https://kuma.arturkamieniecki.pl/status/pieskiuw)

## Webscraper application
The webscraper application uses threads not to halt the main django process. Because it uses them to update the database `celery` and `redis` is needed.
The redis server needs to be set up. Please follow the redis documentation to install the server. If run on ubuntu the redis server can be installed using:  
```bash
$ apt install redis 
```
The celery process also needs to be started with the Django server:
```bash
$ celery -A pieskiUW worker --loglevel=info --concurrency 1 -E
```

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
