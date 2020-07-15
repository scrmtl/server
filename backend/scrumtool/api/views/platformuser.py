from rest_framework import viewsets

from . import models
from . import serializers


class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = models.PlatformUser.objects.all()
    serializer_class = serializers.ScrumUserSerializer
