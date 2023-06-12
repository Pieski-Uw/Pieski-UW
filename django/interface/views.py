from webscraper.models import Pet, PetFoundCords

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    """View of interface index"""
    return render(request, "interface/index.html")


def statistics(request):
    """View of interface statistics"""
    return render(request, "interface/statistics.html")


def map_view(request):
    """View of interface map"""
    return render(request, "interface/map.html")


def estimate(request):
    """View of interface estimate"""
    return render(request, "interface/estimate.html")


def get_animals_number(request):
    """API view that returns the number of animals in the database"""
    pets_number = PetFoundCords.objects.count()
    return JsonResponse({"pets_number": pets_number / 100 + 1})


def get_100_animal_location(request):
    """API view that returns one animal with location"""

    pet_number = request.GET.get("pet_number", None)
    pet_number = int(pet_number) if pet_number is not None else -1

    if pet_number < 0:
        return JsonResponse({"pet": []})

    start = pet_number * 100

    pets = PetFoundCords.objects.all()[start : (start + 99)]
    response = []

    for pet in pets:
        if pet.geo_lat is not None and pet.geo_lng is not None:
            response.append(
                {
                    "name": pet.pet.name,
                    "link": pet.pet.link,
                    "geo_lat": pet.geo_lat,
                    "geo_lng": pet.geo_lng,
                }
            )

    return JsonResponse({"pets": response})


def get_all_animals_locations(request):
    """API view that returns all animals with location"""

    pets = PetFoundCords.objects.all()
    response = []

    for pet in pets:
        if pet.geo_lat is not None and pet.geo_lng is not None:
            response.append(
                {
                    "name": pet.pet.name,
                    "link": pet.pet.link,
                    "geo_lat": pet.geo_lat,
                    "geo_lng": pet.geo_lng,
                }
            )

    return JsonResponse({"pets": response})


def count_pets_by_age(request):
    """API view that counts all pets that have the same age and returns a JSON object"""
    pets_by_age = Pet.objects.values("age").annotate(count=Count("pk"))
    return JsonResponse({"pets_by_age": list(pets_by_age)})


def count_pets_by_weight(request):
    """API view that counts all pets that have the same weight and returns a JSON object"""
    pets_by_weight = Pet.objects.values("weight").annotate(count=Count("pk"))
    return JsonResponse({"pets_by_weight": list(pets_by_weight)})
