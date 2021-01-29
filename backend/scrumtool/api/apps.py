from django.apps import AppConfig
import subprocess
import asyncio
import threading
import logging
from django.conf import settings
stdlogger = logging.getLogger(__name__)


class ApiConfig(AppConfig):
    name = 'api'
    run_already = False
# import signals

    def ready(self):
        if ApiConfig.run_already:
            return
        ApiConfig.run_already = True
        import api.signals
        import planning_poker.signals

        from api.management.commands.runapscheduler import Command
        command = Command()
        x = threading.Thread(target=command.handle)
        x.start()
