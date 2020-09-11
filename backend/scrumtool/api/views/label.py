"""Controller methods in the app for labels
"""
from rest_framework import viewsets, mixins

from .. import models
from .. import serializers
from api.views.nested_ressources_helper import NestedComponentViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class LabelViewSet(AutoPermissionViewSetMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   NestedComponentViewSet):
    """CRUD for Label
    """

    queryset = models.Label.objects.all()
    serializer_class = serializers.LabelSerializer
