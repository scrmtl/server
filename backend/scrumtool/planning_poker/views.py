from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.request import Request

from planning_poker import serializers
from planning_poker import models

from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class PokerVotingViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """
    A viewset that provides information about the requested PokerVoting
    """
    serializer_class = serializers.PokerVotingSerializer
    queryset = models.PokerVoting.objects.all()


class PokerVoteViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """
    A viewset that provides information about the requested PokerVote
    """
    serializer_class = serializers.PokerVoteSerializer
    queryset = models.PokerVote.objects.all()


class VoteViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """
    A viewset that provides information about the requested Vote
    """
    serializer_class = serializers.VoteSerializer
    queryset = models.Vote.objects.all()
