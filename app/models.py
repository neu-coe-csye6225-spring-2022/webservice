import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.utils import timezone


class Healthz(models.Model):
    objects = None


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_updated = models.DateTimeField(default=timezone.now)
    ids = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
