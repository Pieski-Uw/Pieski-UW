from django.shortcuts import render, redirect

from .web_scraper import start_scrapping, kill_scrapping


def refreshDB(request):
    '''View to confirm that one wishes to start scrapping'''
    if request.method == 'POST' and request.POST.get('id', None) == 'refresh':
        start_scrapping()
        return redirect('/')
    return render(request, 'refresh.html', {})

def killScrapping(request):
    '''View to confirm that one wishes to kill scrapping'''
    if request.method == 'POST' and request.POST.get('id', None) == 'kill_scrapping':
        kill_scrapping()
        return redirect('/')
    return render(request, 'kill_scrapping.html', {})

def menu(request):
    '''View of webscrapper menu'''
    return render(request, "index.html", {})