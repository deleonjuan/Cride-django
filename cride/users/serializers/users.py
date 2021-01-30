from rest_framework import serializers 
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from users.models import User

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'username', 'first_name', 'last_name', 'phone_number', 'email' )

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('credenciales invalidas')

        self.context['user'] = user
        return data

    def create(self, data):
        """ generar u obtener nuevo token """
        token, created = Token.objects.get_or_create(user=self.context['user'])

        return self.context['user'], token.key