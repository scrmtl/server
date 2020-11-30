"""Controller methods in the app for cards
"""
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from rest_framework import permissions, status, mixins, generics
from api.views.nested_ressources_helper import NestedComponentViewSet, \
    NestedMtmMixin

from .. import models
from .. import serializers

import logging
logger = logging.getLogger(__name__)


class ProjectViewSet(AutoPermissionViewSetMixin,
                     NestedMtmMixin,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     NestedComponentViewSet):
    """CRUD for Projects
    """

    queryset = models.Project.objects.all()

    def get_queryset(self):
        if self.request.query_params.get('template', False):
            self.queryset = models.Project.template_objects.all()
        else:
            self.queryset = models.Project.objects.all()
        return super().get_queryset()

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
        Add ?template=1 for new project with default template
        Parameters
        ----------
        template: id of the template project 

        Returns
        -------
        Project
            the newly created project
        """
        template = self.request.query_params.get('template', None)
        queryset = self.get_queryset()

        if queryset.filter(id=template).exists():
            new_project_serializer = self.copy_project(template)
            return Response(new_project_serializer.data)
        return super().create(request, *args, **kwargs)

    def list(self, request):
        """Gets the requested queryset for projects

        Parameters
        ----------
        byUser : id of user
        template: set to true to get only 

        Returns
        -------
        Projects
            list of projects
        """
        by_user = self.request.query_params.get('byUser', None)
        _queryset = self.get_queryset().order_by('id')
        current_user: models.PlatformUser = self.request.user

        if by_user is not None and int(by_user) == current_user.id:
            _queryset = self.queryset.filter(
                project_users__plattform_user__id=current_user.id)

        serializer = self.serializer_class(_queryset, many=True)
        return Response(serializer.data)

    def copy_project(self, project_id):
        """
        docstring
        """
        template_project = self.get_queryset().get(
            id=project_id)
        template_project.is_template = False
        new_project_pk = self.deep_copy_model(model=template_project)
        new_project = models.Project.objects.get(pk=new_project_pk)
        new_project_serializer = serializers.ProjectSerializer(
            new_project, data=self.request.data, partial=True)
        if(new_project_serializer.is_valid()):
            new_project_serializer.save()
            self.create_project_user(new_project_pk)
        return new_project_serializer

    def create_project_user(self, project_id):
        plattform_user = self.request.user.id
        role = models.ProjectRole.PO

        return models.ProjectUser.objects.create(
            plattform_user=models.PlatformUser.objects.get(
                id=plattform_user),
            project=models.Project.objects.get(id=project_id),
            role=models.ProjectRole.objects.get(id=role))

    def deep_copy_model(self, model, updated_fk=None, related_field=None,
                        depth: int = 3):
        depth -= 1
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
            if (accessor_name == 'boards' or accessor_name == 'lanes'):
                child_model_relationships.append(
                    (getattr(model, accessor_name).all(), fk_field))

        # Make a copy of the model
        model.pk = None
        model.save()

        # Record the copied model's pk
        new_pk = model.pk
        # Loop through the listed pairs, deep copying each model and passing
        # the pk and field name to update
        if not depth:
            return model.pk
        for child_model_relationship in child_model_relationships:
            for child_model in child_model_relationship[0]:
                self.deep_copy_model(
                    child_model,
                    updated_fk=new_pk,
                    related_field=child_model_relationship[1],
                    depth=depth)

        return model.pk
