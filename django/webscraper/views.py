"""This module defines views for webscraper application"""
from webscraper.tasks import calculate_all_pet_cords

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render

from .web_scraper import kill_scrapping, start_scrapping


@staff_member_required
def refresh_db_view(request):
    """View to confirm that one wishes to start scrapping"""
    if request.method == "POST" and request.POST.get("id", None) == "refresh":
        start_scrapping()
        return redirect("webscraper_menu")
    return render(request, "refresh.html", {})


@staff_member_required
def kill_scrapping_view(request):
    """View to confirm that one wishes to kill scrapping"""
    if request.method == "POST" and request.POST.get("id", None) == "kill_scrapping":
        kill_scrapping()
        return redirect("webscraper_menu")
    return render(request, "kill_scrapping.html", {})


@staff_member_required
def start_calculating_pet_cords(request):
    """View to confirm that one wishes to start calculating pet cords"""
    if (
        request.method == "POST"
        and request.POST.get("id", None) == "start_calculating_pet_cords"
    ):
        calculate_all_pet_cords.delay()
        return redirect("webscraper_menu")
    return render(request, "start_calculating_pet_cords.html", {})


@staff_member_required
def menu(request):
    """View of webscraper menu"""
    return render(request, "index.html", {})
