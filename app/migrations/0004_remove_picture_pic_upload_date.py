# Generated by Django 4.0.2 on 2022-03-09 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='pic_upload_date',
        ),
    ]
