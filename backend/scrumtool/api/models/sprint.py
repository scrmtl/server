""" This file contains database definitions
"""
from rules.contrib.models import RulesModel
import rules
from datetime import date, timedelta

from django.core.exceptions import PermissionDenied
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from simple_history.models import HistoricalRecords

from api.rules_predicates import is_dev_in_project, is_default_user, \
    is_po_in_project, is_sm_in_project, is_project_team_member, is_admin

from api.models.model_interfaces import IGetProject
from api.querysets import SprintQuerySet
import api.models as customModels


class Sprint(RulesModel, IGetProject):
    """Model definition for Sprint."""

    def create_lane_name(self):
        return f'{self.id},Sprint {self.number}: {self.start} - {self.end}'

    def number_default(self):
        """used to calculate the default for the number of the sprint

        Returns
        -------
        int
            Number of current Sprints in this specific project + 1
        """
        no = self.project.sprints.count()
        if no is None:
            return 1
        else:
            return no + 1

    class SprintStatus(models.TextChoices):
        IN_PLANNING = 'IL', _('planning')
        PLANNED = 'PL', _('planned')
        IN_PROGRESS = 'IR', _('in_progress')
        DONE = 'DO', _('done')
        ACCEPTED = 'AC', _('accepted')

    project = models.ForeignKey(
        to="api.Project",
        related_name='sprints',
        on_delete=models.CASCADE,
        help_text='Project this sprint object is part of.')

    history = HistoricalRecords()

    # @property
    # def start(self):
    #    pass
    start = models.DateField(
        blank=True,
        null=True,
        help_text='Begin of the project'
    )
    # @property
    # def end(self):
    #    pass
    end = models.DateField(
        blank=True,
        null=True,
        help_text='End of the project'
    )
    version = models.TextField(
        max_length=12,
        help_text='The Version of the product after the \
            sprint is finished (V00.00.00.00)',
        validators=[
            RegexValidator(r'^V\d{1,2}\.\d{1,2}\.\d{1,2}\.\d{1,2}$')
        ]
    )
    number = models.IntegerField(
        help_text='An ascending number counting the sprint in the project. \
        Starting with 1')

    story = models.TextField(
        help_text='Story of the po that he wants to do in the sprint',
        blank=True,)

    status = models.CharField(choices=SprintStatus.choices,
                              max_length=2,
                              default=SprintStatus.IN_PLANNING)

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'

        rules_permissions = {
            "view": rules.is_authenticated,
            "add": is_default_user,
            "change": is_po_in_project,
            "delete": rules.always_deny,
        }

    def __str__(self):
        """Unicode representation of Project."""
        return "Sprint{0}: {1}  ".format(self.number,
                                         self.id,
                                         )
    timed = SprintQuerySet.as_manager()
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not Sprint.objects.filter(pk=self.id).exists():
            # calculate new Sprint number and date
            project: customModels.Project = self.project
            latest_sprint: Sprint = self.project.latest_sprint
            if not latest_sprint:
                self.number = self.number_default()
                self.start = project.start
            else:
                self.number = latest_sprint.number + 1
                self.start = latest_sprint.end + timedelta(days=1)

            self.end = self.start + timedelta(days=project.sprint_duration)

        super(Sprint, self).save(*args, **kwargs)
