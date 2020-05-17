"""Controller methods in the app for cards
"""
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .. import models
from .. import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD for Projects
    """

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        """retrive for full and partial retrieve
        Add ?DetailLevel=detail for full data
        """
        detaillevel = self.request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'detail':
                instance = self.get_object()
                serializer = serializers.ProjectSerializerFull(instance)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """retrive for full and partial retrieve
        Add ?Template=default for new project with default template
        """
        template = self.request.query_params.get('Template', None)
        name = request.data.get('name')
        description = request.data.get('description')

        if template is not None:
            if template == 'DefaultProject':
                default_project = models.Project.objects.get(
                    name='DefaultProject')
                for board in default_project.boards.all():
                    for lane in board.lanes.all():
                        lane.pk = None
                    board.pk = None
                default_project.pk = None
                default_project.name = name
                default_project.description = description
                default_project.save()
                serializer = serializers.ProjectSerializerFull(
                    data=default_project)
                serializer.is_valid()
                return Response(serializer.data)
        super().create(request, *args, **kwargs)
