from django.contrib import admin
from .models import Profile
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
admin.site.register(Profile)
TokenAdmin.raw_id_fields = ['user']

