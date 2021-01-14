"""Serializers for
"""

import logging
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from api.models import Card, Task, Feature, Epic, Label, File, \
    Steplist, PlatformUser, Lane, Project
from planning_poker.models import PokerVoting, PokerVote, Vote
logger = logging.getLogger(__name__)


class PokerVotingSerializer(
        serializers.ModelSerializer):
    """Base-class serializer for cards.
    Other cards will inherits from this class
    """

    def validate(self, attrs):
        self.date_validator(attrs)
        self.manager_project_member(attrs)
        self.voters_project_members(attrs)
        return attrs

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
        manager = data['manager']
        if Project.objects.filter(project_users__in=manager.project_users.all()).count() > 0:
            return data
        else:
            raise serializers.ValidationError('user not in project')

    def voters_project_members(self, data):
        if not ('voters' in data.keys()):
            raise serializers.ValidationError(
                'please select at least one voter')
        if not ('project' in data.keys()):
            raise serializers.ValidationError('please select a project')
        for voter in data['voters']:
            if Project.objects.filter(
                project_users__in=voter.project_users.all()
            ).count() == 0:
                raise serializers.ValidationError(
                    f'user {voter} not in project')
        return data

    def date_validator(self, data):
        """
        Check that start is before end.
        """
        if (not (('start' in data.keys()) and ('end' in data.keys())) or (
            data['start'] is None or data['end'] is None
        )):
            return data
        if data['start'] > data['end']:
            raise serializers.ValidationError("end must occur after start")
        return data


class PokerVoteSerializer(
        serializers.ModelSerializer):
    """Base-class serializer for cards.
    Other cards will inherits from this class
    """

    avg_storypoints = serializers.SerializerMethodField()
    end_storypoints = serializers.SerializerMethodField()
    act_storypoints = serializers.SerializerMethodField()
    # Storypoints according to fibonacci sequence
    available_storypoints = [1, 2, 3, 5, 8, 13, 21, 34, 55]

    def validate(self, attrs):
        return self.task_unique(attrs)

    class Meta:
        model = PokerVote
        abstract = True
        fields = ('id', 'poker_voting',
                  'task', 'status',
                  'avg_storypoints',
                  'end_storypoints',
                  'act_storypoints'
                  )

    def get_avg_storypoints(self, obj: PokerVote):
        # get tasks of accepted sprints
        if obj.votes.count() == 0:
            return 0
        storypoints = 0
        for vote in obj.votes.all():
            storypoints += vote.storypoints
        return storypoints / obj.votes.count()

    def get_end_storypoints(self, obj: PokerVote):
        if obj.status == PokerVote.PokerStatus.FINISHED:
            sp = round(self.get_avg_storypoints(obj))
            return min(self.available_storypoints, key=lambda x: abs(x-sp))
        else:
            return 0

    def get_act_storypoints(self, obj):
        sp = round(self.get_avg_storypoints(obj))
        return min(self.available_storypoints, key=lambda x: abs(x-sp))

    def task_unique(self, data):
        # get pokervote for same task
        same_vote = PokerVote.objects.filter(task=data['task'])
        if same_vote.exists():
            raise serializers.ValidationError(
                f'A vote for task {data["task"]} already exists ' +
                f'with vote {same_vote.first()}')
        return data


class VoteSerializer(
        serializers.ModelSerializer):
    """Base-class serializer for cards.
    Other cards will inherits from this class
    """

    def validate(self, data):
        if not ('user' in data.keys()):
            raise serializers.ValidationError('please select a user')
        if not ('poker_vote' in data.keys()):
            raise serializers.ValidationError('please select a poker_vote')
        user = data['user']
        poker_vote = data['poker_vote']
        poker_voting = PokerVoting.objects.filter(voters=user,
                                                  id=poker_vote.poker_voting.id
                                                  )
        if poker_voting.count() > 0:
            return data
        else:
            raise serializers.ValidationError(f'User {user} is not member ' +
                                              f'of PokerVoting {poker_voting}')

    class Meta:
        model = Vote
        abstract = True
        fields = ('id', 'poker_vote',
                  'user', 'storypoints'
                  )
