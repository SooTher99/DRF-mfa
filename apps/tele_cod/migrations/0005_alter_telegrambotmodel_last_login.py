# Generated by Django 4.0.4 on 2022-05-31 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tele_cod', '0004_telegrambotmodel_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrambotmodel',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
