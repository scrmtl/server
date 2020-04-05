"""Controller methods in the app for cards
"""
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .. import models
from .. import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD for Projects
    """

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
