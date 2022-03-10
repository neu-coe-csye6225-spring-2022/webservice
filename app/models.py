import os.path
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage

from django.db.models import TextField
from django.db.models.functions import Cast

# Create your models here.
from django.utils import timezone

class Healthz(models.Model):
    objects = None


class Image(models.Model):
    file_name = models.CharField(max_length=100, default='')
    updated_date = models.DateTimeField(auto_now=True)
    ids = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.FileField(null=True, blank=True)
    flag = models.BooleanField(default=False)
    user_id = models.UUIDField(unique=True, null=True)

    def __unicode__(self):
        return self.file_name

    def save(self, *args, **kwargs):
        self.file_name = os.path.basename(self.image.name)
        # items = Cast('id', output_field=TextField())
        new_name = str(self.ids) + "/" + self.file_name
        self.image.name = new_name
        self.flag = True
        super(Image, self).save(*args, **kwargs)


# @receiver(models.signals.post_save, sender=Image)
# def create_update_img_to_s3(sender, instance, created, **kwargs):
#     if instance.image:
#         instance.image.save()

@receiver(models.signals.post_delete, sender=Image)
def delete_img_from_s3(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_updated = models.DateTimeField(default=timezone.now)
    ids = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # Image.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
