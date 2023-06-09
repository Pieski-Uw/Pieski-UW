#!/bin/bash

if [ "${DJANGO_RUN_MIGRATIONS}" = "true" ]; then
    python django/manage.py makemigrations webscraper;
    python django/manage.py makemigrations pieskiUW;
fi;

python django/manage.py migrate --noinput;
python django/manage.py runserver 0.0.0.0:${DJANGO_INTERNAL_PORT}