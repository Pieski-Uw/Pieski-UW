from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("statistics/", views.statistics, name="statistics"),
    path("estimate/", views.estimate, name="estimate"),
    path("update_database/", views.index, name="update_database"),
    path("api/ages/", views.count_pets_by_age, name="API_ages"),
    path("api/weights", views.count_pets_by_weight, name="API_weights"),
    path("api/weights/<int:id>", views.get_pets_by_weight, name="API_get_pets_weight"),
    path("api/ages/<int:id>", views.get_pets_by_age, name="API_get_pets_age"),
]
