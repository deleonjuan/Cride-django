
from rest_framework import serializers

from circles.models import Membership
from users.serializers import UserModelSerializer

class MembershipModelSerializer(serializers.ModelSerializer):

    joined_at = serializers.DateTimeField(source='created', read_only=True)
    user =  UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()

    class Meta:
        model = Membership
        fields = ['user', 'is_admin', 'is_active', 'used_invitations', 'remaining_invitations', 'invited_by', 'rides_taken', 'rides_offered', 'joined_at']
        read_only_fields = ['user', 'used_invitations', 'rides_taken', 'rides_offered']