
from rest_framework import serializers

from rides.models import Ride

from circles.models import Circle, Membership

from datetime import timedelta
from django.utils import timezone

class CreateRideSerializer(serializers.ModelSerializer):

    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)
    
    class Meta:
        model = Ride
        exclude = ['passengers', 'rating', 'is_active', 'offered_in']

    def validate_departure_date(self, data):
        min_date = timezone.now() + timedelta(minutes=10)

        if data < min_date:
            raise serializers.ValidationError('error en fecha de inicio')
        return data

    def validate(self, data):

        if self.context['request'].user != data['offered_by']:
            raise serializers.ValidationError('error en validaion')

        user = data['offered_by']
        circle = self.context['circle']

        try:
            membership = Membership.objects.get(
                user=user, 
                circle=circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('error')

        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError('error en fecha')

        self.context['membership'] = membership
        return data

    def create(self, data):
        
        # circle
        circle = self.context['circle']
        circle.rides_offered += 1
        circle.save()

        #ride
        ride = Ride.objects.create(**data, offered_in=circle)

        # membership
        membership = self.context['membership']
        membership.rides_offered += 1
        membership.save()

        # profile
        profile = data['offered_by'].profile
        profile.rides_offered += 1
        profile.save()

        return ride

class RideModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ['offered_by', 'offered_in', 'rating',]