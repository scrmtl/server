"""Serializers for Projects
"""
from rest_framework import serializers
from ..models import Project
from ..serializers import board_serializers


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Projects.
    """
    boards = board_serializers.BoardSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'description',
                  'boards'
                  )
