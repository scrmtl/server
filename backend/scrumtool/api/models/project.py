""" This file contains database definitions
"""
import math
from rules.contrib.models import RulesModel
import rules
from django.db import models
# Needed for TextChoices
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.core.validators import MinValueValidator, MaxValueValidator

from api.rules_predicates import is_dev_in_project, \
    is_po_in_project, is_sm_in_project, is_project_team_member

from api.models.model_interfaces import IGetProject

import api.models.sprint as customModels

from api.model_managers import TemplateManager


class Project(RulesModel, IGetProject):
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
        help_text='Duration of a sprint in days',
        default=7,
        validators=[MinValueValidator(1), MaxValueValidator(999)]
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
    is_template = models.BooleanField(
        default=False
    )
    objects = models.Manager()
    template_objects = TemplateManager()

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self

    @property
    def latest_sprint(self) -> customModels.Sprint:
        """Getter for the latest sprint of the project
        Returns
        -------
        Sprint
            A Sprint object

        Raises
        ------
        PermissionDenied
            No Permission to enter property
        """
        if not self.sprints.count():
            return None
        else:
            return self.sprints.order_by('-start')[0]

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

        rules_permissions = {
            "view": rules.is_authenticated,
            "add": rules.is_authenticated,
            "change": is_po_in_project,
            "delete": is_po_in_project,
        }

    def __str__(self):
        """Unicode representation of Project."""
        return "{0} ID: {1} ".format(self.name,
                                     self.pk,
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
        else:
            self.numOfSprints = 0

        super(Project, self).save(*args, **kwargs)
