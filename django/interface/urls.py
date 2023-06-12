from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("statistics/", views.statistics, name="statistics"),
    path("estimate/", views.estimate, name="estimate"),
    path("update_database/", views.index, name="update_database"),
    path("map/", views.map_view, name="map"),
    path("api/ages/", views.count_pets_by_age, name="API_ages"),
    path("api/weights", views.count_pets_by_weight, name="API_weights"),
    path("api/locationsAmount", views.get_animals_number, name="API_amount"),
    path("api/locationsOne", views.get_100_animal_location, name="API_locations_one"),
    path("api/locationsAll", views.get_all_animals_locations, name="API_locations_all"),
]
