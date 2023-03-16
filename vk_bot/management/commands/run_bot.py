from dataclasses import asdict

from django.core.management.base import BaseCommand

from vk_bot.bot import VkManager, Poller, Dispatcher
from vk_bot.config import settings

vk_manager = VkManager(settings.VK_API_TOKEN, settings.VK_CLUB_ID, settings.VK_API_VERSION)
dto = vk_manager.get_long_poll_server()
poller = Poller(**asdict(dto))
dispatcher = Dispatcher(vk_manager)
poller.start(dispatcher)


class Command(BaseCommand):
    help = 'Run bot'

    def handle(self, *args, **options):
        poller.start(dispatcher)
