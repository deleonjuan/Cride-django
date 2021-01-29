from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Circle

from .serializers import CircleSerializer, CreateCircleSerializer

# Create your views here.

@api_view(['GET'])
def list_cirles(request):
    """ listar circulos """
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_circle(request):
    """ crear cirulo """
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()

    return Response(CircleSerializer(circle).data)

