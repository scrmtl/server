"""Serializers for Projects
"""
from rest_framework import serializers
from ..models import Project, ProjectUser, Board
from ..serializers import board_serializers, project_user_serializer


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Projects.
    """

    def validate(self, data):
        return date_validator(data)

    def validate_sprint_duration(self, value):
        return sprint_duration_validator(value)

    project_users = serializers.PrimaryKeyRelatedField(
        queryset=ProjectUser.objects.all(),
        required=False,
        many=True)
    boards = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(),
        required=False,
        many=True)

    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'description',
                  'project_users',
                  'start',
                  'end',
                  'sprint_duration',
                  'status',
                  'dor',
                  'dod',
                  'numOfSprints',
                  'boards',
                  'is_template',
                  )
        read_only_fields = ('numOfSprints',)


class ProjectSerializerFull(serializers.ModelSerializer):
    """Serializer for Projects.
    """
    boards = board_serializers.BoardSerializerFull(many=True)
    project_users = project_user_serializer.ProjectUserSerializer(
        many=True,
        required=True)

    def validate(self, data):
        return date_validator(data)

    def validate_sprint_duration(self, value):
        return sprint_duration_validator(value)

    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'description',
                  'project_users',
                  'start',
                  'end',
                  'sprint_duration',
                  'status',
                  'dor',
                  'dod',
                  'numOfSprints',
                  'boards',
                  )
        read_only_fields = ('numOfSprints',)


class ProjectSerializerOnlyId(serializers.ModelSerializer):
    """Serializer for Projects.
    """
    class Meta:
        model = Project
        fields = ('id',
                  )
        read_only_fields = ('id',)


def date_validator(data):
    """
    Check that start is before end.
    """
    if (not (('start' in data.keys()) and ('end' in data.keys()))):
        return data
    if data['start'] > data['end']:
        raise serializers.ValidationError("end must occur after start")
    return data


def sprint_duration_validator(value):
    """Check Sprint duration
    """
    if value <= 0:
        raise serializers.ValidationError(
            "The sprint duration {0} has to be larger than zero".format(value))
    return value
