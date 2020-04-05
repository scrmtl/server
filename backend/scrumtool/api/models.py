""" This file contains database definitions
"""
from django.db import models
from polymorphic.models import PolymorphicModel
# Needed for TextChoices
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """Model definition for Project."""
    name = models.CharField(
        max_length=256,
        help_text='This represents the name of the lane')
    description = models.TextField(
        null=True,
        blank=True,
        help_text='User description of the card')

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        """Unicode representation of Project."""
        return "{0}: {1} ".format(self.name,
                                  self.description
                                  )


BOARD_TYPE = (
    ('PB', 'Product Backlog Board'),
    ('SP', 'Sprint Backlog Board '),
    ('AB', 'Archiv Board'),
)


class Board(models.Model):
    """Model definition for Board."""
    class BoardType(models.TextChoices):
        PB = 'PB', _('Product Backlog Board')
        SP = 'SP', _('Sprint Backlog Board ')
        AB = 'AB', _('Archiv Board')

    board = models.ForeignKey(
        to='Project',
        on_delete=models.CASCADE,
        related_name='boards')
    name = models.CharField(
        max_length=256,
        help_text='This represents the name of the lane')
    description = models.TextField(
        null=True,
        blank=True,
        help_text='User description of the card')
    board_type = models.CharField(
        choices=BoardType.choices,
        max_length=2,
        help_text='This represents the type of board')
    display_lane_horizontal = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Board."""

        verbose_name = 'Board'
        verbose_name_plural = 'Boards'

    def __str__(self):
        """Unicode representation of Board."""
        return "{0}: {1}".format(self.name,
                                 self.description,
                                 )


class Lane(models.Model):
    """Model definition for Lane. """

    board = models.ForeignKey(
        to='Board',
        on_delete=models.CASCADE,
        related_name='lanes')
    name = models.CharField(
        max_length=256,
        help_text='This represents the name of the lane')
    numbering = models.IntegerField(
        default=0,
        help_text='Describes the order of the lanes')

    class Meta:
        """Meta definition for Lane."""

        verbose_name = 'Lane'
        verbose_name_plural = 'Lanes'

    def __str__(self):
        """Unicode representation of Lane."""
        return "{0} with numbering {1}".format(self.name,
                                               self.numbering,
                                               )


class Card(PolymorphicModel):
    """A Card contains all information concerning a task.
    Including the Steplist
    """
    # ForeignKey in abstract classes:
    # https://docs.djangoproject.com/en/dev/topics/db/models/#be-careful-with-related-name-and-related-query-name
    class Status(models.TextChoices):
        NOT_STARTED = 'ns', _('not started')
        DONE = 'do', _('done')
        IN_PROGRESS = 'ip', _('in progress')

    lane = models.ForeignKey(
        to='Lane',
        on_delete=models.CASCADE,
        related_name='%(class)s_cards')
    labels = models.ManyToManyField(
        to='api.Label',
        related_name='%(class)s_cards',
    )
    name = models.CharField(
        max_length=256,
        help_text='User given name of the card')
    description = models.TextField(
        null=True, blank=True,
        help_text='User description of the card')
    numbering = models.IntegerField(
        default=0,
        help_text='Describes the order of the steps')
    storypoints = models.IntegerField(
        default=0,
        help_text='This is the name of the list itself')
    status = models.CharField(
        choices=Status.choices,
        max_length=2,
        default=Status.NOT_STARTED,
        help_text='This is the name of the list itself')

    class Meta:
        """Meta definition for Card."""

        verbose_name = 'Card'
        verbose_name_plural = 'Card'
        abstract = True

    def __str__(self):
        return "{0} ({1}) {2}".format(
            self.name,
            self.description,
            self.storypoints)


class Label(models.Model):
    """Model definition for Label."""
    title = models.CharField(
        max_length=256,
        help_text='This is the text the Label represents')
    color = models.SlugField(
        max_length=6,
        help_text='The color of the label in hex (ffffff)')

    class Meta:
        """Meta definition for Label."""

        verbose_name = 'Label'
        verbose_name_plural = 'Labels'

    def __str__(self):
        """Unicode representation of Label."""
        return "{0} with color {1}".format(self.title,
                                           self.color,

                                           )


class Epic(Card):
    """Model definition for Epic."""

    class Meta:
        """Meta definition for Epic."""

        verbose_name = 'Epic(Card)'
        verbose_name_plural = 'Epics(Card)'


class Feature(Card):
    """A Feature describes a part of an Epic."""
    epic = models.ForeignKey(
        to='Epic',
        on_delete=models.CASCADE,
        related_name='features')

    class Meta:
        """Meta definition for Feature."""
        verbose_name = 'Feature(Card)'
        verbose_name_plural = 'Features(Card)'


class Task(Card):
    """Model definition for Task."""
    feature = models.ForeignKey(
        to='Feature',
        on_delete=models.CASCADE,
        related_name='tasks')

    class Meta:
        """Meta definition for Task."""

        verbose_name = 'Task(Card)'
        verbose_name_plural = 'Tasks(Card)'


class Steplist(models.Model):
    """ A Steplist contains all elements of a Steplist
    """
    task = models.ForeignKey(
        to='Task',
        on_delete=models.CASCADE,
        related_name='steplists')
    name = models.CharField(
        max_length=256,
        default='defaultSteplist',
        help_text='This is the name of the list itself')

    class Meta:
        """Meta definition for Steplist."""

        verbose_name = 'Steplist'
        verbose_name_plural = 'Steplist'

    def __str__(self):
        return "{0} ".format(self.name)


class SteplistItem(models.Model):
    """ A SteplistItem describes a Task that has to be done
    """
    steplist = models.ForeignKey(
        to='Steplist',
        on_delete=models.CASCADE)
    text = models.CharField(
        max_length=256,
        help_text='This is the text the user enters')
    checked = models.BooleanField(
        default=False,
        help_text='Indicates that the step is finished')
    numbering = models.IntegerField(
        default=0,
        unique=False,
        help_text='Describes the order of the steps')

    class Meta:
        """Meta definition for Step."""

        verbose_name = 'Step'
        verbose_name_plural = 'Step'

    def __str__(self):
        return "{0}: {1}({2}): {3} ".format(self.numbering, self.text,
                                            self.steplist,
                                            self.checked,
                                            )
