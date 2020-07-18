"""Serializer for sprints
"""
from datetime import date
from rest_framework import serializers
from api.models import Sprint, Project, Epic, Feature, Task


class SprintSerializer(serializers.ModelSerializer):
    """Serializer for Task-Cards
    """

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=True)
    epic_cards = serializers.PrimaryKeyRelatedField(
        queryset=Epic.objects.all(), required=False, many=True)
    feature_cards = serializers.PrimaryKeyRelatedField(
        queryset=Feature.objects.all(), required=False, many=True)
    task_cards = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), required=False, many=True)
    total_duration = serializers.SerializerMethodField()
    remaining_duration = serializers.SerializerMethodField()

    class Meta:
        model = Sprint
        fields = ('id',
                  'project',
                  'start',
                  'end',
                  'version',
                  'number', 'story',
                  'status',
                  'epic_cards',
                  'feature_cards',
                  'task_cards',
                  'total_duration',
                  'remaining_duration')
        read_only_fields = ('start', 'end', 'number')

    def get_total_duration(self, obj):
        total_duration = 0
        if obj.start is None or obj.end is None:
            return 0
        start = date(obj.start)
        end = date(obj.end)
        total_duration = end - start
        return total_duration

    def get_remaining_duration(self, obj):
        remaining_duration = 0
        if obj.end is None:
            return 0
        start = date.today()
        end = date(obj.end)
        remaining_duration = end - start
        return remaining_duration
