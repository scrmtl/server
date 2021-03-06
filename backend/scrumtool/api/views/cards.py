"""Controller methods in the app for cards
"""
# import the logging library
from api import serializers as apiSerializers
from .. import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions, status, mixins, generics
from api.views.nested_ressources_helper import NestedComponentViewSet, \
    NestedMtmMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from rest_framework.decorators import action
import logging
logger = logging.getLogger(__name__)


class FileViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """CRUD for Files
    """
    queryset = models.File.objects.all()
    serializer_class = apiSerializers.FileSerializer

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = apiSerializers.FileSerializer(data=request.data)
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


class EpicViewSet(AutoPermissionViewSetMixin,
                  NestedMtmMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  NestedComponentViewSet):
    """CRUD for Epics
    """

    queryset = models.Epic.objects.all()

    def get_queryset(self):
        return super().get_queryset()
    serializer_class = apiSerializers.EpicSerializer


class FeatureViewSet(AutoPermissionViewSetMixin,
                     NestedMtmMixin,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     NestedComponentViewSet):
    """CRUD for Features
    """
    queryset = models.Feature.objects.all()

    def get_queryset(self):
        return super().get_queryset()

    serializer_class = apiSerializers.EpicSerializer
    serializer_class = apiSerializers.FeatureSerializer


class TaskViewSet(AutoPermissionViewSetMixin,
                  NestedMtmMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  NestedComponentViewSet):
    """CRUD for Tasks
    """

    queryset = models.Task.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        if "project" in request.query_params:
            data = {
                "project__pk__exact": request.query_params.get('project')}
            filterset = models.TaskCardFilterSet(
                queryset=queryset,
                request=self.request,
                data=data)
            queryset = filterset.qs
        return queryset

    serializer_class = apiSerializers.TaskSerializer

    def retrieve(self, request: Request, *args, pk=None, **kwargs):
        """retrive for full and partial retrieve
            Add ?DetailLevel=full for full data
            """
        detaillevel = request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'full':
                instance = self.get_object()
                serializer = apiSerializers.TaskSerializerFull(instance)
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
                serializer = apiSerializers.TaskSerializerFull(
                    data=request.data)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(
            data=request.data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """update task
            Add ?DetailLevel=full for full data
            """
        super().partial_update(request, args, kwargs)
        detaillevel = self.request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'full':
                instance = self.get_object()
                serializer = apiSerializers.TaskSerializerFull(
                    data=request.data)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def list(self, request, lane_pk=None):
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
        by_user: str = self.request.query_params.get('byUser', None)
        by_lane: str = self.request.query_params.get('byLane', None)
        _queryset = self.get_queryset().order_by('numbering').all()

        current_user: models.PlatformUser = self.request.user
        # needed to evaluate the lazy queryset
        if not _queryset:
            pass
        if (by_user is not None and
            by_user.isdecimal() and
                int(by_user) == current_user.id):
            _queryset = _queryset.filter(
                assigned_users__id=current_user.id)
        elif (by_lane is not None and by_lane.isdecimal()):
            _queryset = _queryset.filter(
                lane__id=int(by_lane))

        serializer = apiSerializers.TaskSerializer(_queryset, many=True)
        return Response(serializer.data)
