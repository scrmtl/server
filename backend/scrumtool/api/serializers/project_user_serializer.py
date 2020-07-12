"""Serializers for ProjectUsers
"""
from rest_framework import serializers
from ..models import ScrumUser, ProjectRole, ProjectUser
from ..serializers import scrumuser_serializer


class ProjectUserSerializer(serializers.ModelSerializer):
    """Serializer for Projects.
    """
    scrum_user = serializers.PrimaryKeyRelatedField(
        queryset=ScrumUser.objects.all(),
        required=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=ProjectRole.objects.all(),
        required=True)
    project = serializers.PrimaryKeyRelatedField(
        queryset=ScrumUser.objects.all(),
        required=True)

    class Meta:
        model = ProjectUser
        fields = ('id',
                  'scrum_user',
                  'role',
                  'project',
                  )
