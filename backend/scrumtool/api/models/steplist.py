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

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

from django.core.validators import RegexValidator
from django.core.exceptions import PermissionDenied

from api.rules_predicates import is_dev_in_project, \
    is_po_in_project, is_sm_in_project, is_project_team_member, is_admin

from api.rules_predicates import can_change_board

from api.models.model_interfaces import IGetProject, IGetBoard


class Steplist(RulesModel, IGetProject, IGetBoard):
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
        rules_permissions = {
            "view": is_project_team_member,
            "add": is_po_in_project,
            "change": can_change_board,
            "delete": is_admin
        }

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

    @property
    def board(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.task.lane.board

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


class SteplistItem(RulesModel, IGetProject, IGetBoard):
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

    @property
    def board(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.steplist.task.lane.board

    class Meta:
        """Meta definition for Step."""

        verbose_name = 'Step'
        verbose_name_plural = 'Step'
        rules_permissions = {
            "view": is_project_team_member,
            "add": is_po_in_project,
            "change": can_change_board,
            "delete": is_admin
        }

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
