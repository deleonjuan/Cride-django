""" users views """
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from users.models import User
from circles.models import Circle

from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from users.permissions import IsAccountOwner

from users.serializers.users import UserLoginSerializer, UserModelSerializer, UserSignupSerializer, AccountVerificationSerializer
from users.serializers.profiles import ProfileModelSerializer
from circles.serializers.circles import CircleModelSerializer


class UserViewSet(
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):


    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field='username'

    def get_permissions(self):
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action == ['retrieve', 'update', 'partial_update']:
            permissions = [IsAccountOwner, IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """
        registrar un nuevo usuario
        """
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        acceso de los usuarios
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'status': 'ok',
            'token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """
        valida a los usuarios por medio del token enviado al correo
        """
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {'message': 'Cuenta verificada'}
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwards):
        response = super(UserViewSet, self).retrieve(request, *args, **kwards)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
            )
        data = {
            'user':response.data,
            'circles':CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):

        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)