"""Serializers for Lanes
"""
from rest_framework import serializers
from ..models import Lane, Task, Feature, Epic, Project
from ..serializers import card_serializers


class LaneSerializer(serializers.ModelSerializer):
    """Serializer for lanes.
    """
    task_cards = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False, many=True)
    epic_cards = serializers.PrimaryKeyRelatedField(
        queryset=Epic.objects.all(),
        required=False, many=True)
    feature_cards = serializers.PrimaryKeyRelatedField(
        queryset=Feature.objects.all(),
        required=False, many=True)

    class Meta:
        model = Lane
        fields = ('id',
                  'name',
                  'numbering',
                  'task_cards',
                  'epic_cards',
                  'feature_cards',
                  )


class LaneSerializerFull(serializers.ModelSerializer):
    """Serializer for lanes.
    """
    epic_cards = card_serializers.EpicSerializer(many=True)
    feature_cards = card_serializers.FeatureSerializer(many=True)
    task_cards = card_serializers.TaskSerializerFull(many=True)
    project = serializers.PrimaryKeyRelatedField(
        required=False, many=False,
        read_only=True)

    class Meta:
        model = Lane
        fields = ('id',
                  'name',
                  'numbering',
                  'epic_cards',
                  'feature_cards',
                  'task_cards',
                  'project'
                  )
