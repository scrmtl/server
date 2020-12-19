from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.request import Request

from scrmtl_statistics import serializers
from api import models


class SprintStatisticViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    A viewset that provides information about the requested Sprint
    """
    serializer_class = serializers.SprintStatisticSerializer
    queryset = models.Sprint.objects.all()

    # def list(self, request: Request):
    """Gets the requested queryset for SprintStatistics

        Parameters
        ----------
        session : if session argument is set return current user info

        Returns
        -------
        Cards
            list of cards
        """
    #   pass

    # def retrieve(self, request: Request, pk=None):
    """retrive for full and partial retrieve
            Instead of id a username can be used
            """
    #    pass


class ProjectStatisticViewSet(mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    """
    A viewset that provides information about the requested Sprint
    """
    serializer_class = serializers.ProjectStatisticSerializer
    queryset = models.Project.objects.all()
