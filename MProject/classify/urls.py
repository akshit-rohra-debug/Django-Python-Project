from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('amazon/',views.amazon,name= 'amazon'),
    path('imdb/',views.imdb,name= 'imdb'),
    path('yelp/',views.yelp,name= 'yelp'),
    ]