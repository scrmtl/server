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
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from rest_framework.decorators import action
import logging
logger = logging.getLogger(__name__)


class FileViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
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


class EpicViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """CRUD for Epics
    """

    queryset = models.Epic.objects.all()
    serializer_class = serializers.EpicSerializer

    @action(methods=['delete'], detail=True)
    def remove_labels_from_task(self, request, pk=None):
        labels_to_remove = request.data['labels']
        for label in labels_to_remove:
            self.remove_label(label)
        return Response(self.serializer_class(self.get_object()).data,
                        status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True)
    def remove_label_from_task(self, request, pk=None):
        label_to_remove = request.data['label']
        self.remove_label(label_to_remove)
        return Response(self.serializer_class(self.get_object()).data,
                        status=status.HTTP_200_OK)

    def remove_label(self, label_data):
        label = get_object_or_404(models.Label, pk=label_data['id'])
        task = self.get_object()
        task.labels.remove(label)
        logger.info('Removed label: %s with from Epic: %s',
                    label, task)


class FeatureViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """CRUD for Features
    """
    queryset = models.Feature.objects.all()
    serializer_class = serializers.FeatureSerializer

    @action(methods=['delete'], detail=True)
    def remove_labels_from_task(self, request, pk=None):
        labels_to_remove = request.data['labels']
        for label in labels_to_remove:
            self.remove_label(label)
        return Response(self.serializer_class(self.get_object()).data,
                        status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True)
    def remove_label_from_task(self, request, pk=None):
        label_to_remove = request.data['label']
        self.remove_label(label_to_remove)
        return Response(self.serializer_class(self.get_object()).data,
                        status=status.HTTP_200_OK)

    def remove_label(self, label_data):
        label = get_object_or_404(models.Label, pk=label_data['id'])
        task = self.get_object()
        task.labels.remove(label)
        logger.info('Removed label: %s with from feature: %s',
                    label, task)


class TaskViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """CRUD for Tasks
    """

    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer

    @action(methods=['delete'], detail=True)
    def remove_labels_from_task(self, request, pk=None):
        labels_to_remove = request.data['labels']
        for label in labels_to_remove:
            self.remove_label(label)
        return Response(serializers.TaskSerializerFull(self.get_object()).data,
                        status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True)
    def remove_label_from_task(self, request, pk=None):
        label_to_remove = request.data['label']
        self.remove_label(label_to_remove)
        return Response(serializers.TaskSerializerFull(self.get_object()).data,
                        status=status.HTTP_200_OK)

    def remove_label(self, label_data):
        label = get_object_or_404(models.Label, pk=label_data['id'])
        task = self.get_object()
        task.labels.remove(label)
        logger.info('Removed label: %s with from task: %s',
                    label, task)

    def retrieve(self, request, *args, pk=None, **kwargs):
        """retrive for full and partial retrieve
            Add ?DetailLevel=full for full data
            """
        detaillevel = self.request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'full':
                instance = self.get_object()
                serializer = serializers.TaskSerializerFull(instance)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, pk=None, **kwargs):
        """update task
            Add ?DetailLevel=full for full data
            """
        detaillevel = self.request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'full':
                instance = self.get_object()
                serializer = serializers.TaskSerializerFull(data=request.data)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = serializers.TaskSerializerFull(
            data=request.data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """update task
            Add ?DetailLevel=full for full data
            """
        detaillevel = self.request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'full':
                instance = self.get_object()
                serializer = serializers.TaskSerializerFull(data=request.data)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = serializers.TaskSerializerFull(
            instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def list(self, request):
        """Gets the requested queryset for cards

        Parameters
        ----------
        byUser : id of user

        byProject : id of project

        Returns
        -------
        Cards
            list of cards
        """
        by_user = self.request.query_params.get('byUser', None)
        by_lane = self.request.query_params.get('byLane', None)
        _queryset = self.queryset
        current_user: models.PlatformUser = self.request.user

        if by_user is not None and int(by_user) == current_user.id:
            _queryset = self.queryset.filter(
                assigned_users__id=current_user.id)
        elif by_lane is not None:
            _queryset = self.queryset.filter(
                lane__id=int(by_lane))

        serializer = self.serializer_class(_queryset, many=True)
        return Response(serializer.data)
