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

    def retrieve(self, request, *args, pk=None, **kwargs):
        """retrive for full and partial retrieve
            Add ?DetailLevel=full for full data
            """
        detaillevel = self.request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'full':
                instance = self.get_object()
                serializer = serializers.BoardSerializerFull(instance)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
