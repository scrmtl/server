"""Serializers for ProjectUsers
"""
from rest_framework import serializers
from ..models import PlatformUser, ProjectRole, ProjectUser, Project
from ..serializers import platformuser_serializer
import logging

stdlogger = logging.getLogger(__name__)


class ProjectUserSerializer(serializers.ModelSerializer):
    """Serializer for Projects.
    """

    def validate(self, data):
        """Check Sprint duration
        """
        project = data['project']
        scrum_user = data['scrum_user']
        for project_user in project.project_users.all():
            if project_user.scrum_user.id == scrum_user.id:
                stdlogger.info(
                    'User is already member of the project %s ',
                    project)
                raise serializers.ValidationError(
                    "User is already member of the project {0} ".format(
                        project))
        return data

    scrum_user = serializers.PrimaryKeyRelatedField(
        queryset=PlatformUser.objects.all(),
        required=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=ProjectRole.objects.all(),
        required=True)
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        required=True)

    class Meta:
        model = ProjectUser
        fields = ('id',
                  'scrum_user',
                  'role',
                  'project',
                  )
