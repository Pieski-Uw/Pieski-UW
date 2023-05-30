import os

from celery import Celery

from django.conf import settings  # pylint: disable=unused-import

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pieskiUW.settings")

app = Celery("pieskiUW")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
