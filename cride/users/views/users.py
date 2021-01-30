""" users views """
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers.users import UserLoginSerializer, UserModelSerializer, UserSignupSerializer, AccountVerificationSerializer

class UserLoginApiView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user, token = serializer.save()

        data = {
            'user': UserModelSerializer(user).data,
            'status': 'ok',
            'token': token
        }

        return Response(data, status=status.HTTP_201_CREATED)
        

class UserSignupApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        data = UserModelSerializer(user).data

        return Response(data, status=status.HTTP_201_CREATED)



class AccountVerificationAPIView(APIView):

    def post(self, request, *args, **kwargs):

        serializer = AccountVerificationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {'message': 'Cuenta verificada'}

        return Response(data, status=status.HTTP_200_OK)