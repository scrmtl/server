"""After card is saves calculate all values together
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

logging.basicConfig(level=logging.DEBUG)
stdlogger = logging.getLogger(__name__)


@receiver(post_save, sender='api.Task')
def run_after_saving_task(sender, **kwargs):
    stdlogger.info("Task changed")

    _feature = sender.feature
    _epic = sender.feature.epic


@receiver(post_save, sender='api.Feature')
def run_after_saving_feature(sender, **kwargs):

    stdlogger.info("Start pre_save Item in signals.py under items app")
    stdlogger.info("sender class %s", (sender.__name__))
    stdlogger.info("sender %s" % (sender))
    stdlogger.info("kwargs %s" % str(kwargs))


@receiver(post_save, sender='api.Epic')
def run_after_saving_epic(sender, **kwargs):

    stdlogger.info("Start pre_save Item in signals.py under items app")
    stdlogger.info("sender class %s" % (sender.__name__))
    stdlogger.info("sender %s" % (sender))
    stdlogger.info("kwargs %s" % str(kwargs))
