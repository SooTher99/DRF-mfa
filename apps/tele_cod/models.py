from django.db import models


class TelegramBotModel(models.Model):
    code = models.IntegerField(max_length='8', blank=True)
    user = models.OneToOneField('default.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Бот"

    def __str__(self):
        return self.user
