# Generated by Django 4.0.4 on 2022-06-07 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('face_auth', '0002_alter_facedescriptionsmodel_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facedescriptionsmodel',
            name='photo',
        ),
    ]
