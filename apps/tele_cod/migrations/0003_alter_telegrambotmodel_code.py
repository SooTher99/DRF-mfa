# Generated by Django 4.0.4 on 2022-05-28 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tele_cod', '0002_telegrambotmodel_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrambotmodel',
            name='code',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Код'),
        ),
    ]
