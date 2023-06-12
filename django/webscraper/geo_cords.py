from geopy.geocoders import ArcGIS
from .models import PetFoundCords, Pet


def calculate_single_pet_cords(pet: Pet):
    """Calculates coordinates of a single pet"""
    if pet.address_found is None:
        # if there is no address found, save this information in database
        pet_found_cords = PetFoundCords(pet=pet, geo_lat=None, geo_lng=None)
        pet_found_cords.save()
        return
    geolocator = ArcGIS()
    location = geolocator.geocode(pet.address_found + "Warszawa")
    if location is None:
        # if cannot find location, save this information in database
        pet_found_cords = PetFoundCords(pet=pet, geo_lat=None, geo_lng=None)
        pet_found_cords.save()
        return
    pet_found_cords = PetFoundCords(
        pet=pet, geo_lat=location.latitude, geo_lng=location.longitude
    )
    pet_found_cords.save()
