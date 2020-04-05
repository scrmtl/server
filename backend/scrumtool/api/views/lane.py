"""Controller methods in the app for cards
"""
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .. import models
from .. import serializers


class LaneViewSet(viewsets.ModelViewSet):
    """CRUD for Lanes
    """

    queryset = models.Lane.objects.all()
    serializer_class = serializers.LaneSerializer
