""" circle urls """

from django.urls import path
from .views import users

urlpatterns = [
    path('user/login/', users.UserLoginApiView.as_view(), name='login'),
]
