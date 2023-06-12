""" This module configures webscraper apps"""
from django.apps import AppConfig


class WebscraperConfig(AppConfig):
    """This class configures webscraper app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "webscraper"
