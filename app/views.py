from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from app.serializers import HealthzSerializer
from app.models import Healthz


class HealthzViewSet(viewsets.ModelViewSet):
    queryset = Healthz.objects.all()
    serializer_class = HealthzSerializer
    http_method_names = ['get']
