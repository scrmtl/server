"""After card is saves calculate all values together
"""
import logging
import sys
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from ..models import Task, Feature, Epic, Card

logging.basicConfig(level=logging.DEBUG)
stdlogger = logging.getLogger(__name__)


@receiver(post_save, sender='api.Task')
@receiver(post_delete, sender='api.Task')
def run_after_saving_task(sender, instance, update_fields, created, **kwargs):
    print('storypoints after save {0}'.format(instance.storypoints))
    print(update_fields)
    print(created)


@receiver(pre_save, sender='api.Task')
@receiver(pre_delete, sender='api.Task')
def run_before_saving_task(sender, **kwargs):
    """Is called when task changes.
    Handels changes in Storypoints.
    """
    new_task = kwargs['instance']
    old_storypoints = -1
    initial_storypoints = 0
    # new calculation of storypoints if storypoints changes or new task added
    if Task.objects.filter(pk=new_task.id).exists():
        old_storypoints = Task.objects.get(pk=new_task.id).storypoints
        old_feature = Task.objects.get(pk=new_task.id).feature
        initial_storypoints = new_task.storypoints - old_storypoints
    else:
        initial_storypoints = new_task.storypoints

    if (new_task.storypoints != old_storypoints or
            new_task.feature != old_feature):
        stdlogger.debug("Storypoints of Task changed")
        str_pt_hdl = StorypointHandler(new_task, initial_storypoints)
        str_pt_hdl.calculateStorypoints()
    else:
        stdlogger.debug("Storypoints of Task didn't change")


class StorypointHandler():
    def __init__(self, card, initial_storypoints=0):
        """creates a StorypointHandler object

        Parameters
        ----------
        card : Task, Feature, Epic
            a Django model that is a child of the card model
        initial_storypoints : int
            Storypoints of an instance that is not yet stored in the database

        Raises
        ------
        TypeError
            wrong datatype of card
        TypeError
            wrong datatype of storypoints
        """
        if isinstance(card, (Card)):
            self.card = card
        else:
            raise TypeError(
                '{card} is not of datatype Card'.format(card=repr(card)))
        if isinstance(initial_storypoints, int):
            self.initial_storypoints = initial_storypoints
        else:
            raise TypeError(
                '{initial_storypoints} is not of datatype int'.format(
                    initial_storypoints=repr(initial_storypoints)))
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
            storypoints += task.storypoints
        return storypoints

    def __get_epic(self):
        if isinstance(self.card, (Task)):
            self.task = self.card
            self.features = self.task.feature
            self.features.storypoints = self.initial_storypoints
            self.epic = self.features.epic
        else:
            raise TypeError(
                '{card} is not of datatype Task'.format(card=repr(self.card)))
