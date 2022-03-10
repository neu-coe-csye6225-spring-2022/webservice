from django.contrib import admin
from .models import Profile, Image
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Image)
TokenAdmin.raw_id_fields = ['user']

