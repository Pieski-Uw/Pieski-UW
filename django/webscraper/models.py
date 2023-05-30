"""This module defines models (and useful functions connected to them),
for webscraper application"""
from django.db import models


class Pet(models.Model):
    """Model of pet table"""

    SEX = (
        ("m", "male"),
        ("f", "female"),
    )
    no = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=100, null=True)
    breed = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, choices=SEX, null=True)
    weight = models.IntegerField(null=True)
    status = models.CharField(max_length=50, null=True)
    date_in = models.DateField(null=True)
    date_out = models.DateField(null=True)
    address_found = models.CharField(max_length=100, null=True)
    box = models.CharField(max_length=50, null=True)
    group_name = models.CharField(max_length=50, null=True)
    group_link = models.URLField(null=True)
    link = models.URLField(null=False)


class WebscrapingProcess(models.Model):
    """Model of process doing the webscrapping"""

    pid = models.IntegerField()
    working = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)


def clear_webscraping_processes():
    """Makes sure there are no redundant PIDs stored in database"""
    procs = WebscrapingProcess.objects.all()
    for process in procs:
        process.delete()
