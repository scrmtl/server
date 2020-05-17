"""Serializers for Boards
"""
from rest_framework import serializers
from ..models import Board
from ..serializers import lane_serializers


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for boards.
    """
    class Meta:
        model = Board
        fields = ('id',
                  'name',
                  'description',
                  'board_type',
                  'display_lane_horizontal',
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
