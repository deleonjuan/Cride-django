from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from circles.permissions import isActiveCircleMember 

from circles.models import Circle
from rides.serializers import CreateRideSerializer

class RideViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    serializer_class = CreateRideSerializer
    permission_classes = [IsAuthenticated, isActiveCircleMember]

    def dispatch(self, request, *args, **kwargs):
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context