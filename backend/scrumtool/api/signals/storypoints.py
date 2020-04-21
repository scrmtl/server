"""After card is saves calculate all values together
"""
from ..models import Task, Feature, Epic, Card
from django.dispatch import receiver
import logging
import sys
from django.db.models import signals

logging.basicConfig(level=logging.DEBUG)
stdlogger = logging.getLogger(__name__)


@receiver(signals.pre_delete, sender='api.Task')
def run_before_delete_task(sender, **kwargs):
    """Is called when task is deleted.
    Handels changes in Storypoints.
    """
    new_task = kwargs['instance']
    # new calculation of storypoints if storypoints changes or new task added
    # old_task = Task.objects.filter(pk=new_task.id)
    # if Task.objects.filter(pk=new_task.id).exists():
    #    new_task.storypoints = 0
    new_task.storypoints = 0
    stdlogger.debug(
        'Storypoints for deleted task %s will be evaluated', new_task)
    str_pt_hdl = StorypointHandler(new_task)
    str_pt_hdl.calculateStorypoints()


@receiver(signals.pre_save, sender='api.Task')
def run_before_saving_task(sender, **kwargs):
    """Is called when task changes.
    Handels changes in Storypoints.
    """
    new_task = kwargs['instance']
    old_storypoints = -1
    # new calculation of storypoints if storypoints changes or new task added
    if Task.objects.filter(pk=new_task.id).exists():
        old_storypoints = Task.objects.get(pk=new_task.id).storypoints
        old_feature = Task.objects.get(pk=new_task.id).feature
    if (new_task.storypoints != old_storypoints or
            new_task.feature != old_feature):
        stdlogger.debug("Storypoints of Task changed")
        str_pt_hdl = StorypointHandler(new_task)
        str_pt_hdl.calculateStorypoints()

    else:
        stdlogger.debug("Storypoints of Task didn't change")


class StorypointHandler():
    def __init__(self, card):
        """creates a StorypointHandler object

        Parameters
        ----------
        card : Task, Feature, Epic
            a Django model that is a child of the card model
        Raises
        ------
        TypeError
            wrong datatype of card
        """
        if isinstance(card, (Card)):
            self.card = card
        else:
            raise TypeError(
                '{card} is not of datatype Card'.format(card=repr(card)))
        self.task = None
        self.features = None
        self.epic = None

    def calculateStorypoints(self):
        self.__get_epic()
        self.__fill_card_classes()

    def __fill_card_classes(self):
        self.features = self.epic.features.all()
        storypoints = 0
        for feature in self.features:
            feature.storypoints = self.__calculate_feature_sp(feature)
            storypoints += feature.storypoints
            feature.save()
        self.epic.storypoints = storypoints
        self.epic.save()

    def __calculate_feature_sp(self, feature):
        storypoints = 0
        for task in feature.tasks.all():
            if task.id == self.task.id:
                storypoints += self.task.storypoints
            else:
                storypoints += task.storypoints
        return storypoints

    def __get_epic(self):
        if isinstance(self.card, (Task)):
            self.task = self.card
            self.features = self.task.feature
            self.epic = self.features.epic
        else:
            raise TypeError(
                '{card} is not of datatype Task'.format(card=repr(self.card)))
