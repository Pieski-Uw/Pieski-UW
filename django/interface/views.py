from webscraper.models import Pet

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    """View of interface index"""
    return render(request, "interface/index.html")


def statistics(request):
    """View of interface statistics"""
    return render(request, "interface/statistics.html")


def estimate(request):
    """View of interface estimate"""
    return render(request, "interface/estimate.html")


def count_pets_by_age(request):
    """API view that counts all pets that have the same age and returns a JSON object"""
    pets_by_age = Pet.objects.values("age").annotate(count=Count("pk"))
    return JsonResponse({"pets_by_age": list(pets_by_age)})


def count_pets_by_weight(request):
    """API view that counts all pets that have the same weight and returns a JSON object"""
    pets_by_weight = Pet.objects.values("weight").annotate(count=Count("pk"))
    return JsonResponse({"pets_by_weight": list(pets_by_weight)})