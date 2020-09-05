"""Controller methods in the app for cards
"""
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, \
    TokenHasScope


from .. import models
from .. import serializers

import logging
logger = logging.getLogger(__name__)


class ProjectViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    """CRUD for Projects
    """

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        """retrive for full and partial retrieve
        Add ?DetailLevel=detail for full data
        """
        # perm = models.Project.get_perm("tester")
        # if request.user.has_perm(models.Project.get_perm("tester")):
        #    print("hello")
        detaillevel = self.request.query_params.get('DetailLevel', None)
        if detaillevel is not None:
            if detaillevel == 'full':
                instance = self.get_object()
                serializer = serializers.ProjectSerializerFull(instance)
                return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """retrive for full and partial retrieve
        Add ?template=DefaultProject for new project with default template
        """
        template = self.request.query_params.get('Template', None)
        name = request.data.get('name')
        description = request.data.get('description')

        if template is not None:
            if template == 'DefaultProject':
                default_project = models.Project.objects.get(
                    name='DefaultProject')
                default_project.name = name
                default_project.description = description
                model_pk = self.deep_copy_model(model=default_project)
                project = models.Project.objects.get(pk=model_pk)
                test_serializer = serializers.ProjectSerializer(project)
                return Response(test_serializer.data)
        super().create(request, *args, **kwargs)

    def list(self, request):
        """Gets the requested queryset for projects

        Parameters
        ----------
        byUser : id of user

        Returns
        -------
        Projects
            list of projects
        """
        by_user = self.request.query_params.get('byUser', None)
        _queryset = self.get_queryset().order_by('id')
        current_user: models.PlatformUser = self.request.user

        if not _queryset:
            pass

        if by_user is not None and int(by_user) == current_user.id:
            _queryset = self.queryset.filter(
                project_users__plattform_user__id=current_user.id)

        serializer = self.serializer_class(_queryset, many=True)
        return Response(serializer.data)

    def deep_copy_model(self, model, updated_fk=None, related_field=None):
        child_model_relationships = []
        # Take the passed in model and get the relationships of that model
        relations = [
            f for f in model._meta.get_fields()
            if (f.one_to_many or f.one_to_one)
            and f.auto_created and not f.concrete
        ]
        # Get the list of related models for those relationships
        for relation in relations:
            accessor_name = relation.get_accessor_name()
            # Get the related field name for each relationship
            fk_field = relation.field.get_attname()
            # Build a list of child model list and related field name pairs
            child_model_relationships.append(
                (getattr(model, accessor_name).all(), fk_field))

        # Make a copy of the model
        model.pk = None

        model.save()

        # Record the copied model's pk
        new_pk = model.pk
        # Loop through the listed pairs, deep copying each model and passing
        # the pk and field name to update
        for child_model_relationship in child_model_relationships:
            for child_model in child_model_relationship[0]:
                self.deep_copy_model(
                    child_model,
                    updated_fk=new_pk,
                    related_field=child_model_relationship[1])

        return model.pk
