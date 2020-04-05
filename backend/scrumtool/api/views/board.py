"""Controller methods in the app for cards
"""
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .. import models
from .. import serializers


class BoardViewSet(viewsets.ModelViewSet):
    """CRUD for Boards
    """

    queryset = models.Board.objects.all()
    serializer_class = serializers.BoardSerializer
