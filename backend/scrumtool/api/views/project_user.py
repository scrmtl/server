"""ViewSet for PlatformUser"""
from rest_framework import viewsets

from . import models
from . import serializers


class ProjectUserViewSet(viewsets.ModelViewSet):
    """ProjectUser ViewSet to return data to REST api
    """
    queryset = models.ProjectUser.objects.all()

    def get_queryset(self):
        if 'project_pk' not in self.kwargs:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(
                project=self.kwargs['project_pk'])
    serializer_class = serializers.ProjectUserSerializer


class ProjectRoleViewSet(viewsets.ModelViewSet):
    """ProjectRole ViewSet to return data to REST api
    """
    queryset = models.ProjectRole.objects.all()
    serializer_class = serializers.ProjectRoleSerializer
