"""Serializer for sprints
"""
from datetime import date
from rest_framework import serializers

from api.models import Sprint, Project, Epic, Feature, Task
from .simple_history_serializers import HistoricalRecordField


class ChangeSerializer(serializers.Serializer):
    diff_changes = serializers.SerializerMethodField()
    history_user = serializers.PrimaryKeyRelatedField(
        queryset=Sprint.history.model.objects.all(), required=False)
    history_date = serializers.DateTimeField()

    def get_diff_changes(self, obj):
        if not obj.prev_record:
            return
        else:
            delta = obj.diff_against(obj.prev_record)
        change_obj = []
        for change in delta.changes:
            changes = {}
            changes["field"] = change.field
            changes["old"] = change.old
            changes["new"] = change.new
            change_obj.append(changes)
        return change_obj


class ChangesListSerializer(serializers.ListSerializer):
    child = ChangeSerializer()


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
    history = ChangesListSerializer(required=False,
                                    read_only=True)

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
                  'remaining_duration',
                  'history')
        read_only_fields = ('start', 'end', 'number')

    def get_total_duration(self, obj: Sprint):
        if obj.project is None:
            return 0
        return obj.project.sprint_duration

    def get_remaining_duration(self, obj: Sprint):
        remaining_duration = 0
        start = date.today()
        end = obj.end
        if (end is None) or (end < start):
            return 0
        remaining_duration = end - start
        return remaining_duration.days
