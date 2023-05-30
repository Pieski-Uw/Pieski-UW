import datetime

from celery import shared_task
from .models import Pet


@shared_task
def create_pet(pet_info, href):  # pet_info is a dictionary as in web_scraper.py
    """Adds a pet to a database from info in a dictionary (parsed from href)"""
    try:
        Pet.objects.get(link=href)
        return  # this animal is already in database!
    except Pet.DoesNotExist:
        pass  # this is a new link to pet!

    if pet_info["gender"] == "samiec":
        gender = "m"
    else:
        gender = "f"

    Pet.objects.create(
        name=pet_info["name"],
        no=pet_info["number"],
        breed=pet_info["breed"],
        gender=gender,
        weight=pet_info["weight"],
        status=pet_info["status"],
        date_in=datetime.datetime.strptime(pet_info["date_in"], "%Y-%m-%d").date(),
        date_out=datetime.datetime.strptime(pet_info["date_out"], "%Y-%m-%d").date(),
        address_found=pet_info["address_found"],
        box=pet_info["box"],
        group_name=pet_info["group_name"],
        group_link=pet_info["group_link"],
        age=pet_info["age"],
        link=href,
    )
