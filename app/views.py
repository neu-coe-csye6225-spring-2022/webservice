from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
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

    def post(self, request, format='json'):
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

            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


