from django.urls import path

from . import views

urlpatterns = [
    path('', views.refreshDB, name='refreshDB'),
]