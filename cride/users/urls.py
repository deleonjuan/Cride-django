""" circle urls """

from django.urls import path
from .views import users

urlpatterns = [
    path('user/login/', users.UserLoginApiView.as_view(), name='login'),
    path('user/signup/', users.UserSignupApiView.as_view(), name='signup'),
    path('user/verify/', users.AccountVerificationAPIView.as_view(), name='verify'),
]
