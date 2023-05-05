from django.shortcuts import render, redirect

from .web_scraper import scrape


def refreshDB(request):
    if request.method == 'POST' and request.POST.get('id', None) == 'refresh':
        scrape()
    return render(request, 'refresh.html', {})