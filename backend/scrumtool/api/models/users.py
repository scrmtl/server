""" This file contains database definitions
"""

from rules.contrib.models import RulesModel, RulesModelBase, RulesModelMixin
import rules
from django.db import models

from django.contrib.auth.models import AbstractUser

from api.rules_predicates import is_dev_in_project, \
    is_po_in_project, is_sm_in_project, is_project_team_member


class ProjectRole(RulesModel):
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

    class Meta:
        """Meta definition for ProjectRule."""
        rules_permissions = {
            "view": rules.always_allow,
            "add": rules.always_deny,
            "change": rules.always_deny,
            "delete": rules.always_deny
        }


class PlatformUser(RulesModelMixin, AbstractUser, metaclass=RulesModelBase):
    '''
    '''
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return "username: {0} (id:{1}) ".format(
            self.username,
            self.id,
        )

    class Meta:
        rules_permissions = {
            "view": rules.always_allow,
            "add": rules.always_allow,
            "change": rules.always_allow,
            "delete": rules.always_allow
        }


class ProjectUser(RulesModel):
    """Model definition for ProjectUser."""
    plattform_user = models.ForeignKey(
        to='PlatformUser',
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

        rules_permissions = {
            "view": is_project_team_member,
            "add": is_po_in_project | is_sm_in_project,
            "change": is_po_in_project | is_sm_in_project,
            "delete": is_po_in_project | is_sm_in_project
        }

    def __str__(self):
        """Unicode representation of ProjectUser."""
        return "User:{0} with role ({1}) in project ({2}) ".format(
            self.plattform_user,
            self.role,
            self.project
        )
