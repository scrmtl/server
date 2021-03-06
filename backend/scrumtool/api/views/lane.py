"""Controller methods in the app for cards
"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions, status, mixins, generics
from api.views.nested_ressources_helper import NestedComponentViewSet, \
    NestedMtmMixin

from django.shortcuts import get_object_or_404
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from .. import models
from .. import serializers


class LaneViewSet(AutoPermissionViewSetMixin,
                  NestedMtmMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  NestedComponentViewSet):
    """CRUD for Lanes
    """

    queryset = models.Lane.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'board_pk' not in self.kwargs:
            request = self.request
            if "project" in self.request.query_params:
                data = {
                    "project__pk__exact": self.request.query_params.get('project')}
                filterset = models.LaneFilterSet(
                    queryset=queryset,
                    request=self.request,
                    data=data)
                queryset = filterset.qs
            return queryset
        else:
            return super().get_queryset().filter(
                board=self.kwargs['board_pk'])
    serializer_class = serializers.LaneSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        """retrive for full and partial retrieve
            Add ?DetailLevel=detail for full data
            """
        detaillevel = self.request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'detail':
                instance = self.get_object()
                serializer = serializers.LaneSerializerFull(instance)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
