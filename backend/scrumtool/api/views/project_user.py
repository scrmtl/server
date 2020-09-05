from rest_framework import viewsets

from . import models
from . import serializers


class ProjectUserViewSet(viewsets.ModelViewSet):
    queryset = models.ProjectUser.objects.all()

    def get_queryset(self):
        if 'project_pk' not in self.kwargs:
            return self.queryset
        else:
            return self.queryset.filter(project=self.kwargs['project_pk'])
    serializer_class = serializers.ProjectUserSerializer
