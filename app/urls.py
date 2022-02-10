from django.urls import include, path

from rest_framework import routers

from app.views import HealthzViewSet

routers = routers.DefaultRouter()
routers.register(r'healthz', HealthzViewSet)

urlpatterns = [
    path('', include(routers.urls))
]
