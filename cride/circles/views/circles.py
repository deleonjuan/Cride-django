from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from circles.models import Circle, Membership
from circles.serializers import CircleModelSerializer

from circles.permissions import isCircleAdmin

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class CircleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    el viewset hereda solo las funciones que necesitamos,
    la funcion delete queda fuera, pues nadie puede eliminar un circulo
    """

    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name' #campo por el que se llaman en vez de id ej. localhost:8000/circles/slug_name/

    def get_permissions(self):
        permissions = [ IsAuthenticated ]

        if self.action in ['update', 'partial_update']:
            permissions.append(isCircleAdmin)
        return [ permission() for permission in permissions ]

    # filtros
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['slug_name', 'name']
    ordering_fields = ['rides_offered', 'rides_taken', 'name']
    filter_fields = ['is_verified', 'is_limited']

    def get_queryset(self):
        queryset = Circle.objects.all()
        # if self.action == 'list':
        #     return queryset.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )
