from django.db import models
from django.utils.translation import gettext_lazy as _


class TelegramBotModel(models.Model):
    code = models.CharField(max_length=12, verbose_name='Код', blank=True, null=True)
    CODE_FIELD = 'code'
    user = models.OneToOneField('default.User', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    user_id_messenger = models.IntegerField(blank=True, null=True, verbose_name='Id мессенджера пользователя')
    user_activation_key = models.CharField(max_length=32, verbose_name='Код активации бота')
    username = models.CharField(max_length=64, blank=True, null=True, verbose_name='Никнейм пользователя')
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Бот"

    def __str__(self):
        return f"{self.username}"
