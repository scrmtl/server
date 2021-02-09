""" This file contains database definitions
"""
import math
from datetime import date
from rules.contrib.models import RulesModel
import rules
from django.db import models
# Needed for TextChoices
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
from django.utils.translation import gettext_lazy as _
from api.models.users import PlatformUser
from django.core.validators import RegexValidator
from django.core.exceptions import PermissionDenied

from simple_history.models import HistoricalRecords

from api.models.model_interfaces import IGetBoard, IGetProject

from api.rules_predicates import can_change_board

from api.rules_predicates import is_dev_in_project, \
    is_po_in_project, is_sm_in_project, is_project_team_member, is_admin, \
    is_default_user

from django_property_filter import PropertyFilterSet, PropertyNumberFilter


class Card(RulesModel, IGetBoard, IGetProject):
    """A Card contains all information concerning a task.
    Including the Steplist
    """
    # ForeignKey in abstract classes:
    # https://docs.djangoproject.com/en/dev/topics/db/models/#be-careful-with-related-name-and-related-query-name
    class Status(models.TextChoices):
        NEW = 'NW', _('new')
        PLANNED = 'PL', _('planned')
        NOT_STARTED = 'NS', _('not started')
        DONE = 'DO', _('done')
        IN_PROGRESS = 'IP', _('in progress')
        ACCEPTED = 'AC', _('accepted')

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
    assigned_users = models.ManyToManyField(
        to='api.PlatformUser',
        related_name='%(class)s_cards',
        blank=True,
        help_text='User that are assigned to the card'
    )
    sprint = models.ForeignKey(
        to="api.Sprint",
        related_name='%(class)s_cards',
        on_delete=models.DO_NOTHING,
        null=True, blank=True,
        help_text='Sprint this card is part of.')
    # to track changes in inheritetd models inherit=True
    history = HistoricalRecords(inherit=True)
    done_on = models.DateField(
        blank=True,
        null=True,
        help_text='Date of task status set to done'
    )

    class Meta:
        """Meta definition for Card."""

        verbose_name = 'Card'
        verbose_name_plural = 'Card'
        abstract = True

    def __str__(self):
        return "ID: {2}, name: {0} (SP: {1})".format(
            self.name,
            self.storypoints,
            self.id)

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.lane.board.project

    @property
    def board(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.lane.board

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


class File(RulesModel):
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
        rules_permissions = {
            "view": is_default_user,
            "add": is_default_user,
            "change": is_default_user,
            "delete": is_default_user
        }

    def __str__(self):
        """Unicode representation of File."""
        return "{0}".format(
            self.photo.name)


class Label(RulesModel):
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
        rules_permissions = {
            "view": is_default_user,
            "add": is_default_user,
            "change": is_default_user,
            "delete": is_default_user
        }

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
        rules_permissions = {
            "view": is_project_team_member,
            "add": is_default_user,
            "change": can_change_board,
            "delete": is_admin
        }


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
        rules_permissions = {
            "view": is_project_team_member,
            "add": is_default_user,
            "change": can_change_board,
            "delete": is_admin
        }


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
        rules_permissions = {
            "view": is_project_team_member,
            "add": is_default_user,
            "change": can_change_board,
            "delete": is_admin
        }


class TaskCardFilterSet(PropertyFilterSet):

    class Meta:
        fields = ['name']
        model = Task
        property_fields = [
            ('project__pk', PropertyNumberFilter, ['exact']),
        ]
