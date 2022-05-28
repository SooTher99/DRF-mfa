import logging
from django.core.management import BaseCommand
from ...tgbot import bot


class Command(BaseCommand):
    help = 'Run bot locally.'
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        bot.bot.delete_webhook()
        self.logger.info('Starting local bot...')
        bot.run()
