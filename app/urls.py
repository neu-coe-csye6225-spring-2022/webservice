from django.urls import include, path, re_path

from rest_framework import routers
from app.views import HealthzViewSet, UserCreate, UserManage, ImageViewSet

routers_healthz = routers.DefaultRouter()
routers_healthz.register(r'health', HealthzViewSet)
routers_img = routers.DefaultRouter()
routers_img.register(r'v1/user/self/pic', ImageViewSet)

# routers_user = routers.DefaultRouter()
# routers_user.register(r'v1/user', UserCreate)


urlpatterns = [
    path('', include(routers_healthz.urls)),  # ip:port/healthz/
    path('', include(routers_img.urls)),
    path('v1/user/', UserCreate.as_view()),  # ip:port/v1/user/
    path('v1/user/self/', UserManage.as_view()),  # ip:port/v1/user/self/
]
