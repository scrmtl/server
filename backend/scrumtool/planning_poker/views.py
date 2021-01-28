from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from planning_poker import serializers
from planning_poker import models

import api.models as api_models

from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class PokerVotingViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """
    A viewset that provides information about the requested PokerVoting
    """
    serializer_class = serializers.PokerVotingSerializer
    queryset = models.PokerVoting.objects.all()

    def create(self, request: Request, *args, **kwargs):
        project_id = request.data.get('project', None)
        if api_models.Project.objects.filter(id=project_id).exists():
            if request.data.get('voters', None) is not None:
                if len(request.data.get('voters')) < 1:
                    project_users = api_models.Project.objects.get(
                        id=project_id).project_users
                    platform_users = api_models.PlatformUser.objects.filter(
                        project_users__in=project_users.all()).values_list(
                        'id', flat=True)
                    platform_users = list(platform_users)
                    data = request.data.copy()
                    data.update({'voters': platform_users})
                    serializer = self.serializer_class(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)

        return super().create(request, *args, **kwargs)


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
