from django.apps import AppConfig
import os
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
        stdlogger.info(
            f"--- ready of App {ApiConfig.name} called --- " +
            f"--- os environment {os.environ.get('RUN_MAIN', None)} --- " +
            f"--- process id: {os.getpid()}")
        if ApiConfig.run_already or os.environ.get('RUN_MAIN', None) != 'true':
            return
        ApiConfig.run_already = True
        import api.signals
        import planning_poker.signals

        from api.management.commands.runapscheduler import Command
        command = Command()
        x = threading.Thread(target=command.handle)
        x.start()
