""" circle urls """

from django.urls import path, include
from .views import users as user_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
]
    
