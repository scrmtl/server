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

    def retrieve(self, request, pk=None, *args, **kwargs):
        """retrive for full and partial retrieve
            """
        detaillevel = self.request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'detail':
                instance = self.get_object()
                serializer = serializers.BoardSerializerFull(instance)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
