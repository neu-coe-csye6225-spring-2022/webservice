from django.urls import include, path, re_path

from rest_framework import routers
from app.views import HealthzViewSet, UserCreate, UserManage

routers_healthz = routers.DefaultRouter()
routers_healthz.register(r'healthz', HealthzViewSet)

# routers_user = routers.DefaultRouter()
# routers_user.register(r'v1/user', UserCreate)


urlpatterns = [
    path('', include(routers_healthz.urls)),  # ip:port/healthz/
    path('v1/user/', UserCreate.as_view()),  # ip:port/v1/user/
    path('v1/user/self/', UserManage.as_view())  # ip:port/v1/user/self/
]
