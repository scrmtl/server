"""ViewSet for PlatformUser"""
from rest_framework import viewsets
from rest_framework import permissions, status, mixins, generics
from api.views.nested_ressources_helper import NestedComponentViewSet, \
    NestedMtmMixin
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from . import models
from . import serializers


class ProjectUserViewSet(AutoPermissionViewSetMixin,
                         NestedMtmMixin,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         NestedComponentViewSet):
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


class ProjectRoleViewSet(AutoPermissionViewSetMixin,
                         NestedMtmMixin,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         NestedComponentViewSet):
    """ProjectRole ViewSet to return data to REST api
    """
    queryset = models.ProjectRole.objects.all()
    serializer_class = serializers.ProjectRoleSerializer
