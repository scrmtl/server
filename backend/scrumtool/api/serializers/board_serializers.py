"""Serializers for Boards
"""
from rest_framework import serializers
from ..models import Board, Lane, Project
from ..serializers import lane_serializers


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for boards.
    """
    lanes = serializers.PrimaryKeyRelatedField(
        queryset=Lane.objects.all(), required=False, many=True)
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=False)

    class Meta:
        model = Board
        fields = ('id',
                  'name',
                  'description',
                  'board_type',
                  'display_lane_horizontal',
                  'lanes',
                  'project'
                  )


class BoardSerializerFull(serializers.ModelSerializer):
    """Serializer for boards.
    """
    lanes = lane_serializers.LaneSerializerFull(many=True)

    class Meta:
        model = Board
        fields = ('id',
                  'name',
                  'description',
                  'board_type',
                  'display_lane_horizontal',
                  'lanes'
                  )
