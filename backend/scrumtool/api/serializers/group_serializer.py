"""Serializers for Groups
"""

from rest_framework import serializers
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Group
    """
    class Meta:
        model = Group
        fields = ('id', 'name',)
