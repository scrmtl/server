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
    can_change_board, is_own_profile

from api.models.model_interfaces import IGetProject, IGetBoard


class PokerVoting(RulesModel, IGetProject):
    """Model definition for Board."""
    class VotingMode(models.TextChoices):
        ASYNC = 'ASYNC', _('Asynchronous')
        SYNC = 'SYNC', _('Synchronous')

    project = models.ForeignKey(
        to='api.Project',
        on_delete=models.CASCADE,
        related_name='poker_votings',
        help_text='The project this PokerVoting belongs to',
    )
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
    mode = models.CharField(
        choices=VotingMode.choices,
        max_length=5,
        default=VotingMode.ASYNC,
        help_text='This represents the type of the voting.'
    )
    manager = models.ForeignKey(
        to='api.PlatformUser',
        on_delete=models.CASCADE,
        related_name='poker_voting_managers',
        help_text='The project this PokerVoting belongs to',
    )
    voters = models.ManyToManyField(
        blank=True,
        null=True,
        to='api.PlatformUser',
        related_name='poker_voting_voters',
        help_text='The project this PokerVoting belongs to',
    )

    class Meta:
        """Meta definition for PokerVoting."""

        verbose_name = 'PokerVoting'
        verbose_name_plural = 'PokerVotings'

        rules_permissions = {
            "view": is_project_team_member,
            "add": is_po_in_project | is_sm_in_project,
            "change": is_po_in_project | is_sm_in_project,
            "delete": rules.always_deny
        }

    def __str__(self):
        """Unicode representation of Board."""
        return "PokerVoting ID: {0}".format(self.id,
                                            )

    def save(self, *args, **kwargs):
        if self.voters is None:
            project_users = self.project.project_users
            platform_users = PlatformUser.objects.filter(
                project_users__in=project_users.all())
            for platform_user in platform_users.all():
                self.voters.add(platform_user)
                print(self.voters.all())
            self.save(force_update=True)
            print(self.voters.all())


class PokerVote(RulesModel, IGetProject):
    """Model definition for PokerVote."""
    class PokerStatus(models.TextChoices):
        ACCEPTED = 'AC', _('Accepted')
        FINISHED = 'FIN', _('Finished')  # when all player voted
        WAITING = 'WAIT', _('Waiting')  # When at least one player voted
        SKIPPED = 'SKIP', _('Skipped')
        NOTSTARTED = 'NS', _('not started')

    poker_voting = models.ForeignKey(
        to='planning_poker.PokerVoting',
        on_delete=models.CASCADE,
        related_name='poker_votes',
        help_text='The PokerVoting this PokerVoter belongs to',
    )
    task = models.ForeignKey(
        to='api.Task',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='poker_votes',
        help_text='The PokerVoting this PokerVoter belongs to',
    )
    status = models.CharField(
        choices=PokerStatus.choices,
        max_length=4,
        default=PokerStatus.NOTSTARTED,
        help_text='This represents the status of the vote.'
    )

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.poker_voting.project

    class Meta:
        """Meta definition for PokerVote."""

        verbose_name = 'PokerVote'
        verbose_name_plural = 'PokerVotes'

        rules_permissions = {
            "view": is_project_team_member,
            "add": is_po_in_project | is_sm_in_project,
            "change": is_po_in_project | is_sm_in_project,
            "delete": is_po_in_project | is_sm_in_project
        }

    def __str__(self):
        """Unicode representation of PokerVote."""
        return "PokerVote ID: {0} for task {1}".format(self.id, self.task
                                                       )


class Vote(RulesModel, IGetProject):
    """Model definition for Vote."""
    poker_vote = models.ForeignKey(
        to='planning_poker.PokerVote',
        on_delete=models.CASCADE,
        related_name='votes',
        help_text='The PokerVote this Vote belongs to',
    )
    user = models.ForeignKey(
        to='api.PlatformUser',
        on_delete=models.CASCADE,
        related_name='votes',
        help_text='The project this PokerVoting belongs to',
    )
    storypoints = models.IntegerField(
        default=0,
        help_text='Storypoints the user voted for the PokerVote')

    @property
    def project(self):
        """Getter for the parent project

        Returns
        -------
        Project
            The parent Project
        """
        return self.poker_vote.project

    class Meta:
        """Meta definition for Vote."""

        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

        rules_permissions = {
            "view": is_own_profile,
            "add": is_own_profile,
            "change": is_own_profile,
            "delete": is_own_profile
        }

    def __str__(self):
        """Unicode representation of PokerVote."""
        return "Vote ID: {0} for pokerVote {1}".format(self.id, self.poker_vote
                                                       )
