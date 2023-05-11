"""This module defines urls for webscraper"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("refresh/", views.refresh_db_view, name="refresh_db_view"),
    path("kill/", views.kill_scrapping_view, name="kill_scrapping_view"),
]
