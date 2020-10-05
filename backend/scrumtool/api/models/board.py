""" This file contains database definitions
"""
from rules.contrib.models import RulesModel
import rules
from django.db import models
# Needed for TextChoices
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
from django.utils.translation import gettext_lazy as _


from django.core.validators import RegexValidator
from django.core.exceptions import PermissionDenied

from api.rules_predicates import is_dev_in_project, \
    is_po_in_project, is_sm_in_project, is_project_team_member, is_admin,\
    can_change_board

from api.models.model_interfaces import IGetProject, IGetBoard


class Board(RulesModel, IGetProject, IGetBoard):
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

    @property
    def board(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self

    class Meta:
        """Meta definition for Board."""

        verbose_name = 'Board'
        verbose_name_plural = 'Boards'

        rules_permissions = {
            "view": is_project_team_member,
            "add": is_po_in_project,
            "change": can_change_board,
            "delete": is_admin
        }

    def __str__(self):
        """Unicode representation of Board."""
        return "{0} ID: {1}".format(self.name,
                                    self.id,
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
