"""This module defines urls for webscraper"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="webscraper_menu"),
    path("refresh/", views.refresh_db_view, name="refresh_db_view"),
    path("kill/", views.kill_scrapping_view, name="kill_scrapping_view"),
    path(
        "start_calculating_pet_cords/",
        views.start_calculating_pet_cords,
        name="start_calculating_pet_cords",
    ),
]
