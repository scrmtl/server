"""Serializers for ProjectUsers
"""
from rest_framework import serializers
from ..models import PlatformUser, ProjectRole, ProjectUser, Project
from ..serializers import platformuser_serializer
from django.utils.translation import gettext_lazy as _
import logging

stdlogger = logging.getLogger(__name__)


class ProjectUserSerializer(serializers.ModelSerializer):
    """Serializer for Projects.
    """

    def validate(self, data):
        """Check Sprint duration
        """
        project = data.get('project', None)
        plattform_user = data.get('plattform_user', None)
        if (project and plattform_user):
            for project_user in project.project_users.all():
                if project_user.plattform_user.id == plattform_user.id:
                    stdlogger.info(
                        'User is already member of the project %s ',
                        project)
                    raise serializers.ValidationError(
                        _('User is already member of the project: {0}').format(
                            project)
                    )
        return data

    plattform_user = serializers.PrimaryKeyRelatedField(
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
                  'plattform_user',
                  'role',
                  'project',
                  )


class ProjectRoleSerializer(serializers.ModelSerializer):
    """Serializer for ProjectRoles.
    """
    role_name = serializers.CharField(source='get_id_display')

    class Meta:
        model = ProjectRole
        fields = ('id',
                  'role_name',
                  )
