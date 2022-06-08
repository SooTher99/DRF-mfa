from django.db import models
from django.contrib.postgres.fields import ArrayField


def upload_to(instance, filename):
    return f'images/{filename}'


class FaceDescriptionsModel(models.Model):
    description = ArrayField(models.FloatField())
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    user = models.OneToOneField('default.User', on_delete=models.CASCADE,
                                verbose_name='Пользователь')

    class Meta:
        verbose_name = "Описание лица"
        verbose_name_plural = "Описание лиц"

    def __str__(self):
        return f"{self.user}"
