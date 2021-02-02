from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from circles.permissions import isActiveCircleMember 

from circles.models import Circle
from rides.serializers import CreateRideSerializer, RideModelSerializer

from datetime import timedelta
from django.utils import timezone

class RideViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    # serializer_class = CreateRideSerializer
    permission_classes = [IsAuthenticated, isActiveCircleMember]

    def dispatch(self, request, *args, **kwargs):
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateRideSerializer
        return RideModelSerializer

    def get_queryset(self):
        offset = timezone.now() + timedelta(minutes=10)
        return self.circle.ride_set.filter(
            departure_date__gte=offset,
            is_active=True,
            available_seats__gte=1
        )
    