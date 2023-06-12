"""This module defines views for webscraper application"""
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
def menu(request):
    """View of webscraper menu"""
    return render(request, "index.html", {})
