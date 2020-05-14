"""Controller methods in the app for labels
"""
from rest_framework import viewsets

from .. import models
from .. import serializers


class LabelViewSet(viewsets.ModelViewSet):
    """CRUD for Label
    """

    queryset = models.Label.objects.all()
    serializer_class = serializers.LabelSerializer
