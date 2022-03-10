from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from app.models import Healthz, Image


class HealthzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Healthz
        fields = ()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    username = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    account_created = serializers.DateTimeField(read_only=True, required=False)
    account_updated = serializers.DateTimeField(read_only=True, required=False)

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['username'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'])

        return user

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'password', 'username', 'date_joined', 'account_created', 'account_updated')
