"""Serializers for Boards
"""
from rest_framework import serializers
from ..models import Board


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for boards.
    """
    class Meta:
        model = Board
        fields = ('id',
                  'name',
                  'description',
                  'board_type',
                  'display_lane_horizontal'
                  )
