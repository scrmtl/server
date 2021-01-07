from django.apps import AppConfig
import subprocess
import asyncio
import threading
import logging
from django.conf import settings
stdlogger = logging.getLogger(__name__)


class ApiConfig(AppConfig):
    name = 'api'

# import signals
    def ready(self):
        import api.signals
        from api.management.commands.runapscheduler import Command
        command = Command()
        x = threading.Thread(target=command.handle)
        x.start()
        # asyncio.run(self.run_app_scheduler())

    async def run_app_scheduler(self):
        from api.management.commands.runapscheduler import Command
        command = Command()
        await command.handle()
        stdlogger.error("app_scheduler stopped")
