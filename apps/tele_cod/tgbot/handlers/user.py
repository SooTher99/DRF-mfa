from telebot import TeleBot
from telebot.types import Message
from ...models import TelegramUsersModel


def send_welcome(message: Message, bot:TeleBot):
    bot.reply_to(message, "Здравствуйте, введите ваш пароль")


# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)


def auth(message: Message, bot: TeleBot):
    user = TelegramUsersModel.objects.filter(password=message.text).first()
    if user:
        if user.tg_id == message.from_user.id:
            bot.reply_to(message, "Вы уже авторизованы")

        elif user.password == message.text and user.tg_id is None:
            user.tg_id = message.from_user.id
            user.chat_id = message.chat.id
            user.is_active = True
            user.first_name = message.from_user.first_name
            user.last_name = message.from_user.last_name
            user.username = message.from_user.username
            user.save()
            bot.reply_to(message, f'Вы авторизовались {message.from_user.id}')

        elif user.tg_id != message.from_user.id:
            bot.reply_to(message, "Пароль уже активирован")
    else:
        bot.reply_to(message, "Неправильный пароль")
