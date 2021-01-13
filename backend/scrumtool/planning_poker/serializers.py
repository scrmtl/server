"""Serializers for
"""
import logging
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from api.models import Card, Task, Feature, Epic, Label, File, \
    Steplist, PlatformUser, Lane, Project
from planning_poker.models import PokerVoting, PokerVote, Vote
logger = logging.getLogger(__name__)


class PokerVotingSerializer(serializers.ModelSerializer):
    """Base-class serializer for cards.
    Other cards will inherits from this class
    """

    def validate(self, data):
        self.manager_project_member(data)
        self.voters_project_members(data)

    class Meta:
        model = PokerVoting
        abstract = True
        fields = ('id',
                  'project',
                  'start',
                  'end',
                  'mode',
                  'manager',
                  'voters',
                  )

    def manager_project_member(self, data):
        if not ('manager' in data.keys()):
            raise serializers.ValidationError('please select a manager')
        if not ('project' in data.keys()):
            raise serializers.ValidationError('please select a project')
        manager = get_object_or_404(PlatformUser, id=data['manager'])
        if len(Project.filter(project_users__in=manager.project_users)) > 0:
            return
        else:
            raise serializers.ValidationError('user not in project')

    def voters_project_members(self, data):
        if not ('voters' in data.keys()):
            raise serializers.ValidationError(
                'please select at least one voter')
        if not ('project' in data.keys()):
            raise serializers.ValidationError('please select a project')
        for voter_id in data['manager']:
            voter = get_object_or_404(PlatformUser, id=voter_id)
            if len(Project.filter(project_users__in=voter.project_users)) > 0:
                return
            else:
                raise serializers.ValidationError('user not in project')


class PokerVoteSerializer(serializers.ModelSerializer):
    """Base-class serializer for cards.
    Other cards will inherits from this class
    """

    avg_storypoints = serializers.SerializerMethodField()
    end_storypoints = serializers.SerializerMethodField()
    act_storypoints = serializers.SerializerMethodField()

    class Meta:
        model = PokerVote
        abstract = True
        fields = ('id', 'poker_voting',
                  'task', 'status',
                  'avg_storypoints',
                  'end_storypoints',
                  'act_storypoints'
                  )

    def get_avg_storypoints(self, obj):
        return 9999

    def get_end_storypoints(self, obj):
        return 9999

    def get_act_storypoints(self, obj):
        return 9999


class VoteSerializer(serializers.ModelSerializer):
    """Base-class serializer for cards.
    Other cards will inherits from this class
    """

    def validate_user(self, data):
        if not ('user' in data.keys()):
            raise serializers.ValidationError('please select a user')
        if not ('poker_vote' in data.keys()):
            raise serializers.ValidationError('please select a poker_vote')
        manager = get_object_or_404(PlatformUser, id=data['user'])
        poker_vote = get_object_or_404(PokerVote, id=data['poker_vote'])
        if len(poker_vote.poker_voting.filter(voters__pk=user)) > 0:
            return
        else:
            raise serializers.ValidationError('user not in project')

    class Meta:
        model = Vote
        abstract = True
        fields = ('id', 'poker_vote',
                  'user', 'storypoints'
                  )
