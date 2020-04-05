"""Controller methods in the app for cards
"""
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .. import models
from .. import serializers


class EpicViewSet(viewsets.ModelViewSet):
    """CRUD for Epics
    """

    queryset = models.Epic.objects.all()
    serializer_class = serializers.EpicSerializer


class FeatureViewSet(viewsets.ModelViewSet):
    """CRUD for Features
    """

    queryset = models.Feature.objects.all()
    serializer_class = serializers.FeatureSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD for Tasks
    """

    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
