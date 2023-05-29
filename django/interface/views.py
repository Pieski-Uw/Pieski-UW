from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from webscraper.models import Pet


def index(request):
    return render(request, 'interface/index.html')

def statistics(request):
    return render(request, 'interface/statistics.html')

def estimate(request):
    return render(request, 'interface/estimate.html')


def count_pets_by_age(request):
    """API view that counts all pets that have the same age and returns a JSON object"""
    pets_by_age = Pet.objects.values('age').annotate(count=Count('pk'))
    return JsonResponse({'pets_by_age': list(pets_by_age)})

def count_pets_by_weight(request):
    """API view that counts all pets that have the same weight and returns a JSON object"""
    pets_by_weight = Pet.objects.values('weight').annotate(count=Count('pk'))
    return JsonResponse({'pets_by_weight': list(pets_by_weight)})