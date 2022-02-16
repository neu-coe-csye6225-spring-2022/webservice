from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone

from app.serializers import HealthzSerializer, UserSerializer
from app.models import Healthz


class HealthzViewSet(viewsets.ModelViewSet):
    queryset = Healthz.objects.all()
    serializer_class = HealthzSerializer
    http_method_names = ['get']


class UserCreate(APIView):
    """
    Create a user
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                output = {
                    'id': user.profile.ids,
                    'first_name': serializer.data['first_name'],
                    'last_name': serializer.data['last_name'],
                    'username': serializer.data['username'],
                    'account_created': serializer.data['date_joined'],
                    'account_updated': user.profile.account_updated
                }
                return Response(
                    output,
                    status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
