""" This file contains database definitions
"""
from django.db import models
# Needed for TextChoices
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

from django.core.validators import RegexValidator
from django.core.exceptions import PermissionDenied

from datetime import date
import math


class Project(models.Model):
    """Model definition for Project."""
    class ProjectStatus(models.TextChoices):
        AR = 'AR', _('Archiv')
        AC = 'AC', _('Active')

    name = models.CharField(
        max_length=256,
        help_text='This represents the name of the lane')
    description = models.TextField(
        null=True,
        blank=True,
        help_text='User description of the card')
    start = models.DateField(
        blank=True,
        null=True,
        help_text='Begin of the project'
    )
    end = models.DateField(
        blank=True,
        null=True,
        help_text='End of the project'
    )
    sprint_duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Duration of a sprint in days'
    )
    status = models.CharField(
        choices=ProjectStatus.choices,
        max_length=2,
        default=ProjectStatus.AC,
        help_text='This represents the type of board')
    dor = models.TextField(
        null=True,
        blank=True,
        help_text='Definition of Ready ')
    dod = models.TextField(
        null=True,
        blank=True,
        help_text='Definition of Done ')
    numOfSprints = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Number of Sprints possible '
    )

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        """Unicode representation of Project."""
        return "{0}: {1} Description:{2}  ".format(self.name,
                                                   self.pk,
                                                   self.description,

                                                   )

    def save(self, *args, **kwargs):
        if Project.objects.filter(pk=self.id).exists():
            old_proj = Project.objects.get(pk=self.id)
        if (self.status == self.ProjectStatus.AR and
                old_proj.status == self.ProjectStatus.AR):
            raise PermissionDenied(
                'Can\'t modify because board has {0} status'.format(
                    self.status))
        # calculate number of Sprints in this project
        if (self.sprint_duration is not None and
            self.start is not None and
                self.end is not None):
            delta = self.end - self.start
            self.numOfSprints = math.floor((delta.days / self.sprint_duration))
        super(Project, self).save(*args, **kwargs)


class Board(models.Model):
    """Model definition for Board."""
    class BoardType(models.TextChoices):
        PB = 'PB', _('Product Backlog Board')
        SP = 'SP', _('Sprint Backlog Board ')
        AB = 'AB', _('Archiv Board')

    project = models.ForeignKey(
        to='Project',
        on_delete=models.CASCADE,
        related_name='boards',
        help_text='The project this board belongs to',
    )
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

    def save(self, *args, **kwargs):
        # if Project.objects.filter(pk=self.id).exists():
        #    old_proj = Project.objects.get(pk=self.id)
        if ((self.project_id is not None) and
                (self.project.status == self.project.ProjectStatus.AR)):
            raise PermissionDenied(
                'Can\'t modify because board has {0} status'.format(
                    self.project.status))
        super(Board, self).save(*args, **kwargs)


class Lane(models.Model):
    """Model definition for Lane. """

    board = models.ForeignKey(
        to='Board',
        on_delete=models.CASCADE,
        related_name='lanes',
        help_text='The board this lane is associated with'
    )
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

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.board.project

    def save(self, *args, **kwargs):
        # if Project.objects.filter(pk=self.id).exists():
        #    old_proj = Project.objects.get(pk=self.id)
        if ((self.board_id is not None) and
                (self.project.status == self.project.ProjectStatus.AR)):
            raise PermissionDenied(
                'Can\'t modify because board has {0} status'.format(
                    self.project.status))
        super(Lane, self).save(*args, **kwargs)


class Card(models.Model):
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
        related_name='%(class)s_cards',
        help_text='Lane this card belongs to'
    )
    labels = models.ManyToManyField(
        to='api.Label',
        related_name='%(class)s_cards',
        blank=True,
        help_text='User defined label for the card'
    )
    files = models.ManyToManyField(
        to='api.File',
        related_name='%(class)s_files',
        blank=True,
        help_text='Files a user wants to be connected with the card',
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

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.lane.board.project

    def save(self, *args, **kwargs):
        # if Project.objects.filter(pk=self.id).exists():
        #    old_proj = Project.objects.get(pk=self.id)
        if ((self.lane_id is not None) and
            (self.project.status ==
                self.project.ProjectStatus.AR)):
            raise PermissionDenied(
                'Can\'t modify because board has {0} status'.format(
                    self.project.status))
        super(Card, self).save(*args, **kwargs)


class File(models.Model):
    """Model definition for File."""
    photo = models.ImageField(
        upload_to='card_attachement')

    class Meta:
        """Meta definition for File."""

        # def update(self, request, pk=None, **kwargs):
        verbose_name = 'File'
    #     if pk is None:
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     labels = request.data.get('labels')
    #     if (labels is not None):
    #         i = 0
    #         for label in labels:
    #             label_serializer = serializers.LabelSerializer(data=label)
    #             if label_serializer.is_valid():
    #                 logger.info('Save new label: %s' %
    #                             label_serializer.validated_data)
    #                 label_serializer.save()
    #                 labels[i] = label_serializer.data
    #                 i += 1
    #     request.data['labels'] = labels
    #     super().update(request)
        verbose_name_plural = 'Files'

    def __str__(self):
        """Unicode representation of File."""
        return "{0}".format(
            self.photo.name)


class Label(models.Model):
    """Model definition for Label."""
    title = models.CharField(
        max_length=256,
        help_text='This is the text the Label represents')
    color = models.TextField(
        max_length=7,
        help_text='The color of the label in hex (#ffffff)',
        validators=[
            RegexValidator('^#[A-Fa-f0-9]{6}$')
        ]
    )

    class Meta:
        """Meta definition for Label."""

        verbose_name = 'Label'
        verbose_name_plural = 'Labels'

    def __str__(self):
        """Unicode representation of Label."""
        return "{0} with color {1} id: {2}".format(
            self.title,
            self.color,
            self.id,
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
        related_name='features',
        blank=True,)

    class Meta:
        """Meta definition for Feature."""
        verbose_name = 'Feature(Card)'
        verbose_name_plural = 'Features(Card)'


class Task(Card):
    """Model definition for Task."""
    feature = models.ForeignKey(
        to='Feature',
        on_delete=models.CASCADE,
        related_name='tasks',
        blank=True,)

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
        return "{0} id:{1}".format(self.name, self.pk)

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.task.lane.board.project

    def save(self, *args, **kwargs):
        # if Project.objects.filter(pk=self.id).exists():
        #    old_proj = Project.objects.get(pk=self.id)

        # Check if board is in Archive
        if ((self.task_id is not None) and
            (self.project.status ==
                self.project.ProjectStatus.AR)):
            raise PermissionDenied(
                'Can\'t modify because board has {0} status'.format(
                    self.task.lane.board.project.status))
        super(Steplist, self).save(*args, **kwargs)


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

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.steplist.task.lane.board.project

    class Meta:
        """Meta definition for Step."""

        verbose_name = 'Step'
        verbose_name_plural = 'Step'

    def __str__(self):
        return "{0}: {1}(steplist:{2}) id:{3} ".format(
            self.numbering, self.text,
            self.steplist,
            self.id,
        )

    def save(self, *args, **kwargs):
        # if Project.objects.filter(pk=self.id).exists():
        #    old_proj = Project.objects.get(pk=self.id)
        if ((self.steplist_id is not None) and
            (self.project.status ==
             self.project.ProjectStatus.AR)):
            raise PermissionDenied(
                'Can\'t modify because board has {0} status'.format(
                    self.steplist.task.lane.board.project.status))
        super(SteplistItem, self).save(*args, **kwargs)


class ProjectRole(models.Model):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''
    PO = 1
    SM = 2
    DEV = 3
    ROLE_CHOICES = (
        (PO, 'product owner'),
        (SM, 'scrum master'),
        (DEV, 'developer'),
    )
    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, primary_key=True)

    @property
    def is_po(self):
        if self.id == 1:
            return True
        else:
            return False

    @property
    def is_sm(self):
        if self.id == 2:
            return True
        else:
            return False

    @property
    def is_dev(self):
        if self.id == 3:
            return True
        else:
            return False

    def __str__(self):
        return self.get_id_display()


class ScrumUser(AbstractUser):
    '''

    '''
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return "username: {0} (id:{1}) ".format(
            self.username,
            self.id,
        )


class ProjectUser(models.Model):
    """Model definition for ProjectUser."""
    scrum_user = models.ForeignKey(
        to='ScrumUser',
        on_delete=models.DO_NOTHING,
        related_name='project_users'
    )
    role = models.ForeignKey(
        to='ProjectRole',
        on_delete=models.DO_NOTHING,
        related_name='project_users'
    )
    project = models.ForeignKey(
        to='Project',
        on_delete=models.DO_NOTHING,
        related_name='project_users'
    )

    class Meta:
        """Meta definition for ProjectUser."""

        verbose_name = 'ProjectUser'
        verbose_name_plural = 'ProjectUsers'

    def __str__(self):
        """Unicode representation of ProjectUser."""
        return "User:{0} with role ({1}) in project ({2}) ".format(
            self.scrum_user,
            self.role,
            self.project
        )
