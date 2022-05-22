from django.db import models


class TelegramBotModel(models.Model):
    code = models.IntegerField(max_length=8, blank=True, null=True)
    user = models.OneToOneField('default.User', on_delete=models.CASCADE)
    user_id_messenger = models.IntegerField(blank=True, null=True)
    user_activation_key = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Бот"

    def __str__(self):
        return self.user
