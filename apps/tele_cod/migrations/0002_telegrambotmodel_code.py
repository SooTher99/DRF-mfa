# Generated by Django 4.0.4 on 2022-05-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tele_cod', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrambotmodel',
            name='code',
            field=models.CharField(default=0, max_length=12, verbose_name='Код'),
            preserve_default=False,
        ),
    ]
