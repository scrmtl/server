"""Serializers for Lanes
"""
from rest_framework import serializers
from ..models import Lane


class LaneSerializer(serializers.ModelSerializer):
    """Serializer for lanes.
    """
    class Meta:
        model = Lane
        fields = ('id',
                  'name',
                  'numbering',
                  )
