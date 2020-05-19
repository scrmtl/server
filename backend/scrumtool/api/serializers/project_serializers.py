"""Serializers for Projects
"""
from rest_framework import serializers
from ..models import Project
from ..serializers import board_serializers


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Projects.
    """

    def validate(self, data):
        return date_validator(data)

    def validate_sprint_duration(self, value):
        return sprint_duration_validator(value)

    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'description',
                  'start',
                  'end',
                  'sprint_duration',
                  'status',
                  'dor',
                  'dod',
                  'numOfSprints',
                  )
        read_only_fields = ('numOfSprints',)


class ProjectSerializerFull(serializers.ModelSerializer):
    """Serializer for Projects.
    """
    boards = board_serializers.BoardSerializerFull(many=True)

    def validate(self, data):
        return date_validator(data)

    def validate_sprint_duration(self, value):
        return sprint_duration_validator(value)

    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'description',
                  'start',
                  'end',
                  'sprint_duration',
                  'status',
                  'dor',
                  'dod',
                  'numOfSprints',
                  'boards'
                  )
        read_only_fields = ('numOfSprints',)


"""Serializers for readonly
"""


class ProjectSerializerReadOnly(ProjectSerializer):
    """Serializer for Projects.
    """
    class Meta:
        read_only_fields = ('id',
                            'name',
                            'description',
                            'start',
                            'end',
                            'sprint_duration',
                            'status',
                            'dor',
                            'dod',
                            'numOfSprints',)


class ProjectSerializerFullReadOnly(ProjectSerializerFull):
    """Serializer for Projects.
    """
    class Meta:
        read_only_fields = ('id',
                            'name',
                            'description',
                            'start',
                            'end',
                            'sprint_duration',
                            'status',
                            'dor',
                            'dod',
                            'numOfSprints',
                            'boards')


def date_validator(data):
    """
    Check that start is before end.
    """
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
