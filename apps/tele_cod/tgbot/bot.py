# filters
from .filters.admin_filter import AdminFilter

# handlers
from .handlers.admin import admin_user
from .handlers.spam_command import anti_spam
from .handlers.user import send_welcome, auth

# middlewares
from .middlewares.antiflood_middleware import antispam_func

# states
from .states.register_state import Register

# utils
# from .utils.database import Database

# telebot
from telebot import TeleBot

# config
from . import config

# db = Database()

# remove this if you won't use middlewares:
from telebot import apihelper

apihelper.ENABLE_MIDDLEWARE = True

# I recommend increasing num_threads
bot = TeleBot(config.TOKEN, num_threads=5)


def register_handlers():
    bot.register_message_handler(admin_user, commands=['start'], admin=True, pass_bot=True)
    bot.register_message_handler(send_welcome, commands=['start'], admin=False, pass_bot=True)
    bot.register_message_handler(anti_spam, commands=['spam'], pass_bot=True)
    bot.register_message_handler(auth, func=lambda message: True, pass_bot=True)


register_handlers()

# Middlewares
bot.register_middleware_handler(antispam_func, update_types=['message'])

# custom filters
bot.add_custom_filter(AdminFilter())


def run():
    bot.infinity_polling()

