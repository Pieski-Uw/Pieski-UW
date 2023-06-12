from webscraper.models import Pet, PetFoundCords

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.db.models.manager import BaseManager

NUMBER_OF_PETS_NEEDED_FOR_ESTIMATE = 10
"""The number of pets needed to estimate the average stay in the shelter.
The number 10 was selected to eliminate queries where the number of pets is too low
for a good estimate."""


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
    """View of interface estimate
    This function calculates the average stay of pets in the shelter based on the
    get parameters.
    If there are not enough pets to estimate the range is increased until there are
    NUMBER_OF_PETS_NEEDED_FOR_ESTIMATE pets. Otherwise error is displayed.
    If an estimate was calculated some example pets are displayed."""

    breeds = Pet.objects.values("breed").exclude(breed="").distinct()

    filters = {
        "breed": request.GET.get("breed"),
        "age": request.GET.get("age"),
        "weight": request.GET.get("weight"),
        "gender": request.GET.get("sex"),
    }

    if filters["gender"] is not None:
        filters["gender"] = filters["gender"].lower()

    min_age = None
    max_age = None
    min_weight = None
    max_weight = None

    pets = Pet.objects.all()

    if not (
        (filters["breed"] is None)
        and (filters["age"] is None)
        and (filters["weight"] is None)
        and (filters["gender"] is None)
    ):
        if filters["breed"] is not None and filters["breed"] != "":
            pets = Pet.objects.filter(breed=filters["breed"])
        if filters["gender"] is not None and filters["gender"] != "":
            pets = pets.filter(gender=filters["gender"])
        if filters["age"] is not None and filters["age"] != "":
            min_age = int(filters["age"])
            max_age = int(filters["age"])
        if filters["weight"] is not None and filters["weight"] != "":
            min_weight = int(filters["weight"])
            max_weight = int(filters["weight"])

    if pets.count() < NUMBER_OF_PETS_NEEDED_FOR_ESTIMATE:
        context = {
            "breeds": breeds,
            "error": "Not enough pets to estimate",
        }
        context.update(filters)
        return render(request, "interface/estimate.html", context)

    filtered_pets = filter_pets(pets, min_age, max_age, min_weight, max_weight)

    sum_days = 0
    pets_skipped = 0
    for pet in filtered_pets:
        if pet.date_in is None or pet.date_out is None:
            pets_skipped += 1
            continue
        sum_days += (pet.date_out - pet.date_in).days

    if filtered_pets.count() - pets_skipped < NUMBER_OF_PETS_NEEDED_FOR_ESTIMATE:
        context = {"breeds": breeds, "error": "Not enough pets to estimate"}
    else:
        context = {
            "breeds": breeds,
            "estimate": int(sum_days / (filtered_pets.count() - pets_skipped)),
            "example_pets": filtered_pets.order_by("?")[:9],
        }

    context.update(filters)

    return render(request, "interface/estimate.html", context)


def filter_pets(pets: BaseManager[Pet], min_age, max_age, min_weight, max_weight):
    """Filters pets based on the given parameters.
    If there are not enough pets to estimate the range is increased until there are
    NUMBER_OF_PETS_NEEDED_FOR_ESTIMATE pets."""

    filtered_pets = pets

    while True:
        if min_age is not None:
            filtered_pets = filtered_pets.filter(age__gte=min_age, age__lte=max_age)
            if min_weight is not None:
                filtered_pets = filtered_pets.filter(
                    weight__gte=min_weight, weight__lte=max_weight
                )
        elif min_weight is not None:
            filtered_pets = filtered_pets.filter(
                weight__gte=min_weight, weight__lte=max_weight
            )

        if filtered_pets.count() >= NUMBER_OF_PETS_NEEDED_FOR_ESTIMATE:
            break

        if min_age is not None and max_age is not None:
            min_age -= 1
            max_age += 1

        if min_weight is not None and max_weight is not None:
            min_weight -= 1
            max_weight += 1

    return filtered_pets


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


def get_pets_by_weight(request, key):
    """API view that returns in JSON all pets that have weight = id"""
    pets = serializers.serialize("json", Pet.objects.filter(weight=key))
    return JsonResponse({"pets": pets})


def get_pets_by_age(request, key):
    """API view that returns in JSON all pets that have age = id"""
    pets = serializers.serialize("json", Pet.objects.filter(age=key))
    return JsonResponse({"pets": pets})
