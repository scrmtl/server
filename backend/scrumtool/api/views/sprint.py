"""Controller methods in the app for cards
"""
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from api import models
from api import serializers


class SprintViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """CRUD for Sprints
    """

    queryset = models.Sprint.objects.all()
    serializer_class = serializers.SprintSerializer
