"""Serializers for Lanes
"""
from rest_framework import serializers
from ..models import Lane
from ..serializers import card_serializers


class LaneSerializer(serializers.ModelSerializer):
    """Serializer for lanes.
    """
    epic_cards = card_serializers.EpicSerializer(many=True)
    feature_cards = card_serializers.FeatureSerializer(many=True)
    task_cards = card_serializers.TaskSerializer(many=True)

    class Meta:
        model = Lane
        fields = ('id',
                  'name',
                  'numbering',
                  'epic_cards',
                  'feature_cards',
                  'task_cards',
                  )
