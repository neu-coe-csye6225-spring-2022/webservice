from rest_framework import serializers

from app.models import Healthz


class HealthzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Healthz
        fields = ()
