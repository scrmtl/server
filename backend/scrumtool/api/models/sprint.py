""" This file contains database definitions
"""
from rules.contrib.models import RulesModel
import rules

from django.core.exceptions import PermissionDenied

from api.rules_predicates import is_dev_in_project, \
    is_po_in_project, is_sm_in_project, is_project_team_member

from api.models.model_interfaces import IGetProject


class Sprint(RulesModel, IGetProject):
    """Model definition for Project."""

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'

        rules_permissions = {
            "view": rules.is_authenticated,
            "add": rules.is_authenticated,
            "change": is_po_in_project,
            "delete": is_po_in_project,
        }

    def __str__(self):
        """Unicode representation of Project."""
        return "{0}: {1} Description:{2}  ".format(self.name,
                                                   self.pk,
                                                   self.description,

                                                   )
