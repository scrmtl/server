"""Controller methods in the app for groups
"""
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django.contrib.auth.models import Group

from .. import serializers


class GroupViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """List and Retrieve for Groups
    """

    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
