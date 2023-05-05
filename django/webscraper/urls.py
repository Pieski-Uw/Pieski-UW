from django.urls import path

from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('refresh/', views.refreshDB, name='refreshDB'),
    path('kill/', views.killScrapping, name='killScrapping'),
]