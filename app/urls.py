from django.urls import include, path, re_path

from rest_framework import routers

from app.views import HealthzViewSet, UserCreate

routers_healthz = routers.DefaultRouter()
routers_healthz.register(r'healthz', HealthzViewSet)

# routers_user = routers.DefaultRouter()
# routers_user.register(r'v1/user', UserCreate)


urlpatterns = [
    path('', include(routers_healthz.urls)),  # ip:port/healthz/
    re_path(r'v1/', UserCreate.as_view(), name='user'),  # ip:port/v1/user/
]
