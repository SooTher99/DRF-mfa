# Generated by Django 4.0.4 on 2022-06-07 15:18

import apps.face_auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facedescriptionsmodel',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=apps.face_auth.models.upload_to),
        ),
    ]
