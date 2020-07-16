from rest_framework import viewsets

from . import models
from . import serializers


class ProjectUserViewSet(viewsets.ModelViewSet):
    queryset = models.ProjectUser.objects.all()
    serializer_class = serializers.ProjectUserSerializer
