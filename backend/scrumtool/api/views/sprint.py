"""Controller methods in the app for cards
"""
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, mixins, generics
from api.views.nested_ressources_helper import NestedComponentViewSet, \
    NestedMtmMixin

from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from api import models
from api import serializers


class SprintViewSet(AutoPermissionViewSetMixin,
                    NestedMtmMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    NestedComponentViewSet):
    """CRUD for Sprints
    """

    queryset = models.Sprint.objects.all()

    def get_queryset(self):
        if 'project_pk' not in self.kwargs:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(project=self.kwargs['project_pk'])
    serializer_class = serializers.SprintSerializer
