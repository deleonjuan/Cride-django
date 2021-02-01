""" circle urls """

from django.urls import path, include
from .views import circles as circles_views
from .views import memberships as membership_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'circles', circles_views.CircleViewSet, basename='circle')
router.register(
    r'circles/(?P<slug_name>[-a-zA-Z0-0_]+)/members', membership_views.MembershipViewSet, basename='members' 
)

urlpatterns = [
    path('', include(router.urls)),
]
