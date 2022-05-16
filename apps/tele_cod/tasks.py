from celery import shared_task
# from .tgbot2 import main_bot
from .tgbot.bot import main_bot


@shared_task
def start_bot():
    main_bot()

# @shared_task
# def start_bot2():
#     main_bot.start()


