""" circle urls """

from django.urls import path
from .views import list_cirles, create_circle

urlpatterns = [
    path('circles/', list_cirles),
    path('circles/create/', create_circle),
]
