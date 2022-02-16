from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from app.models import Healthz
from util.bcrypt_salt_hash_pw import BcryptUtil


class HealthzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Healthz
        fields = ()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, required=False, format='hex_verbose')
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
                                        password=BcryptUtil.get_hashed_pw(validated_data['password']))

        return user

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'password', 'username',
                  'account_created', 'account_updated')
