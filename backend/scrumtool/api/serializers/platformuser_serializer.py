"""Serializer for PlatformUser
    """
from rest_framework import serializers
from django.contrib.auth.models import Group
from .. import models


class PlatformUserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
        many=True)

    class Meta:
        model = models.PlatformUser
        fields = ('id',
                  'email',
                  'username',
                  'name',
                  'groups')
