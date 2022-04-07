import statsd

# Create your views here.
from rest_framework import viewsets, status, parsers
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone

from app.serializers import HealthzSerializer, UserSerializer, ImageSerializer
from app.models import Healthz, Image

metric_counter = statsd.client.StatsClient('localhost', 8125)


class HealthzViewSet(viewsets.ModelViewSet):
    queryset = Healthz.objects.all()
    serializer_class = HealthzSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        metric_counter.incr("health_endpoint")
        return Response([], status=status.HTTP_200_OK)


class ImageViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'delete']

    def attempt_create(self, count, request, *args, **kwargs):
        user = request.user
        if user:
            request.data['user_id'] = user.profile.ids
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            output = {
                'file_name': serializer.data['file_name'],
                'id': serializer.data['ids'],
                'url': serializer.data['image'],
                'upload_date': serializer.data['updated_date'],
                'user_id': serializer.data['user_id'],
            }
            return Response(output, status=status.HTTP_201_CREATED, headers=headers)
        elif count < 5:
            print("delete the existed image and upload")
            Image.objects.get(user_id=request.data['user_id']).delete()
            return self.attempt_create(count + 1, request, *args, **kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        metric_counter.incr("add_or_update_a_profile_pic")
        return self.attempt_create(0, request, args, kwargs)

    def list(self, request, *args, **kwargs):
        metric_counter.incr("get_profile_image")
        user = request.user
        if user:
            user_id = user.profile.ids
            for img_obj in Image.objects.all():
                if img_obj.user_id == user_id:
                    serializer = self.get_serializer(img_obj)
                    output = {
                        'file_name': serializer.data['file_name'],
                        'id': serializer.data['ids'],
                        'url': serializer.data['image'],
                        'upload_date': serializer.data['updated_date'],
                        'user_id': serializer.data['user_id'],
                    }
                    return Response(output, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        metric_counter.incr("delete_profile_pic")
        user = request.user
        if user:
            user_id = user.profile.ids
            for img_obj in Image.objects.all():
                print(img_obj.user_id)
                if img_obj.user_id == user_id:
                    self.perform_destroy(img_obj)
                    return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)


class UserCreate(APIView):
    """
    Create a user
    """

    def post(self, request, format='json'):
        metric_counter.incr("create_a_user")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                user.profile.account_updated = serializer.data['date_joined']
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


class UserManage(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        metric_counter.incr("get_user_information")
        user = request.user
        output = {}
        if user:
            output['id'] = user.profile.ids
            output['first_name'] = user.first_name
            output['last_name'] = user.last_name
            output['username'] = user.username
            output['account_created'] = user.date_joined
            output['account_updated'] = user.profile.account_updated

        return Response(output, status=status.HTTP_200_OK)

    def put(self, request, format='json'):
        metric_counter.incr("update_user_information")
        user = request.user
        if request.data is not None and user:
            for k, v in request.data.items():
                if v is None:
                    continue

                if k == 'first_name':
                    user.first_name = v
                elif k == 'last_name':
                    user.last_name = v
                elif k == 'password':
                    user.set_password(v)
                # elif k == 'username':
                #     continue
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            user.profile.account_updated = timezone.now().isoformat()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
