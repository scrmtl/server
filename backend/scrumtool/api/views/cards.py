"""Controller methods in the app for cards
"""
# import the logging library
from .. import serializers
from .. import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import viewsets
import logging
logger = logging.getLogger(__name__)


class FileViewSet(viewsets.ModelViewSet):
    """CRUD for Files
    """
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = serializers.FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            for k, v in kwargs.items():
                for id in v.split(','):
                    obj = get_object_or_404(models.File, pk=int(id))
                    self.perform_destroy(obj)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class EpicViewSet(viewsets.ModelViewSet):
    """CRUD for Epics
    """

    queryset = models.Epic.objects.all()
    serializer_class = serializers.EpicSerializer


class FeatureViewSet(viewsets.ModelViewSet):
    """CRUD for Features
    """

    queryset = models.Feature.objects.all()
    serializer_class = serializers.FeatureSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD for Tasks
    """

    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
