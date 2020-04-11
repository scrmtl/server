"""After card is saves calculate all values together
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

stdlogger = logging.getLogger(__name__)


@receiver(post_save, sender='items.Item')
def run_before_saving(sender, **kwargs):

    stdlogger.info("Start pre_save Item in signals.py under items app")
    stdlogger.info("sender class %s" % (sender.__name__))
    stdlogger.info("sender %s" % (sender))
    stdlogger.info("kwargs %s" % str(kwargs))
