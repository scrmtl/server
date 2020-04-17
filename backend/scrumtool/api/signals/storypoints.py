"""After card is saves calculate all values together
"""
import logging
import sys
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from ..models import Task, Feature, Epic, Card

logging.basicConfig(level=logging.DEBUG)
stdlogger = logging.getLogger(__name__)


@receiver(pre_save, sender='api.Task')
@receiver(pre_delete, sender='api.Task')
def run_after_saving_task(sender, **kwargs):
    """Is called when task changes.
    Handels changes in Storypoints.
    """

    stdlogger.info("Task changed")
    str_pt_hdl = StorypointHandler(sender)
    str_pt_hdl.calculateStorypoints()
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


class StorypointHandler():
    def __init__(self, card):
        print(type(Task))
        print(type(card))
        print(isinstance(card, 'Task'))
        if isinstance(card, (Task, Feature, Task)):
            self.card = card
        else:
            raise TypeError(
                '{card} is not of datatype Card'.format(card=repr(card)))
        self.task = None
        self.feature = None
        self.epic = None

    def calculateStorypoints(self):
        self.__fill_card_classes()

    def __fill_card_classes(self):
        if isinstance(self.card, Task):
            self.task = self.card
            self.feature = self.task.feature
            self.epic = self.feature.epic
        if isinstance(self.card, Feature):
            pass
        if isinstance(self.card, Epic):
            pass
