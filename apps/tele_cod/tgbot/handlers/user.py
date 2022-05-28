from telebot import TeleBot
from telebot.types import Message
from ...models import TelegramBotModel


def send_welcome(message: Message, bot:TeleBot):
    bot.reply_to(message, "Здравствуйте, введите ваш пароль")


# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)


def auth(message: Message, bot: TeleBot):
    user = TelegramBotModel.objects.filter(user_activation_key=message.text).first()
    if user:
        if user.user_id_messenger == message.from_user.id:
            bot.reply_to(message, "Этот Telegram аккаунт уже авторизован")

        elif user.user_activation_key == message.text and user.user_id_messenger is None:
            user.user_id_messenger = message.from_user.id
            user.username = message.from_user.username
            user.save()
            bot.reply_to(message, f'Вы авторизовались {message.from_user.username}')

        elif user.user_id_messenger != message.from_user.id:
            bot.reply_to(message, "Пароль уже активирован")
    else:
        bot.reply_to(message, "Неправильный пароль")
