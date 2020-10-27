""" This file contains database definitions
"""

from rules.contrib.models import RulesModel
import rules

from api.models import Project, Board, IGetProject, IGetBoard
from django.db import models

from django.core.exceptions import PermissionDenied

from api.rules_predicates import is_dev_in_project, \
    is_po_in_project, is_sm_in_project, is_project_team_member, \
    can_change_board, is_admin

from django_property_filter import PropertyFilterSet, PropertyNumberFilter


class Lane(RulesModel, IGetProject, IGetBoard):
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

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.board.project

    class Meta:
        """Meta definition for Lane."""

        verbose_name = 'Lane'
        verbose_name_plural = 'Lanes'
        rules_permissions = {
            "view": is_project_team_member,
            "add": is_po_in_project,
            "change": can_change_board,
            "delete": is_admin
        }

    def __str__(self):
        """Unicode representation of Lane."""
        return "{0} ID: {2}with numbering {1}".format(self.name,
                                                      self.numbering,
                                                      self.id,
                                                      )

    def save(self, *args, **kwargs):
        # if Project.objects.filter(pk=self.id).exists():
        #    old_proj = Project.objects.get(pk=self.id)
        if ((self.board_id is not None) and
                (self.project.status == self.project.ProjectStatus.AR)):
            raise PermissionDenied(
                'Can\'t modify because board has {0} status'.format(
                    self.project.status))
        super(Lane, self).save(*args, **kwargs)


class LaneFilterSet(PropertyFilterSet):

    class Meta:
        fields = ['name']
        model = Lane
        property_fields = [
            ('project__id', PropertyNumberFilter, ['exact']),
        ]
