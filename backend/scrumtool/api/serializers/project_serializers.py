"""Serializers for Projects
"""
from rest_framework import serializers
from ..models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Projects.
    """
    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'description',
                  )
