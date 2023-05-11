"""This module defines models (and useful functions connected to them),
for webscraper application"""
import datetime
from django.db import models


# model was previously in pieskiUW.models, but models shouldn't
# be kept in a project directory. Read more:
# https://stackoverflow.com/questions/2610727/django-project-models-py-versus-app-models-py#:~:text=Django%20models%20can%20only%20reside%20in%20applications%2C%20not,in%20the%20places%20where%20it%20would%20make%20sense.
# Credit for creating model to jpalikowska
class Pet(models.Model):
    """Model of pet table"""

    SEX = (
        ("m", "male"),
        ("f", "female"),
    )
    no = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=SEX)
    weight = models.IntegerField()
    status = models.CharField(max_length=50)
    date_in = models.DateField()
    date_out = models.DateField()
    address_found = models.CharField(max_length=100)
    box = models.CharField(max_length=50)
    group_name = models.CharField(max_length=50)
    group_link = models.URLField()
    link = models.URLField()


class WebscrappingProcess(models.Model):
    """Model of process doing the webscrapping"""

    pid = models.IntegerField()
    working = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)


# delete all WebscrappingProcess objects
def clear_webscrapping_processes():
    """Makes sure there are no redundant PIDs stored in database"""
    procs = WebscrappingProcess.objects.all()
    for process in procs:
        process.delete()


def create_pet(pet_info, href):  # pet_info is a dictionary as in web_scraper.py
    """Adds a pet to a database from info in a dictionary (parsed from href)"""
    try:
        Pet.objects.get(link=href)
        return  # this animal is already in database!
    except Pet.DoesNotExist:
        pass  # this is a new link to pet!

    if pet_info.gender == "samiec":
        gender = "m"
    else:
        gender = "f"

    Pet.objects.create(
        name=pet_info.name,
        no=pet_info.number,
        breed=pet_info.breed,
        gender=gender,
        weight=pet_info.weight,
        status=pet_info.status,
        date_in=datetime.datetime.strptime(pet_info.date_in, "%Y-%m-%d").date(),
        date_out=datetime.datetime.strptime(pet_info.date_out, "%Y-%m-%d").date(),
        address_found=pet_info.address_found,
        box=pet_info.box,
        group_name=pet_info.group_name,
        group_link=pet_info.group_name,
        link=href,
    )
