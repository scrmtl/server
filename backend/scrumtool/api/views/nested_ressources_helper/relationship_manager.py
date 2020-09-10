"""Helper for nested ressources like Tasks/1/?Label=1
Only Provides Create and delete
    """
from django.http import Http404
from django.shortcuts import get_object_or_404
import logging
from rest_framework.request import Request
from rest_framework import viewsets
logger = logging.getLogger(__name__)


class NestedMtMViewSet(viewsets.ModelViewSet):

    def partial_update(self, request: Request, *args, **kwargs):
        """Adds an element to the specified many to many relation

        Parameters
        ----------
        request : Request
            Has to provide items in query_params (key, value)

        example:
        ---> tasks/1/?labels=1

        """
        instance = self.get_object()
        for key, value in request.query_params.items():
            if hasattr(instance, key):
                getattr(instance, key).add(value)
        if not request.query_params.dict():
            return super().partial_update(request, args, kwargs)
        instance.save()
        return self.get_serializer(instance)

    def destroy(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        for key, value in request.query_params.items():
            if hasattr(instance, key):
                getattr(instance, key).remove(value)
        if not request.query_params.dict():
            return super().partial_update(request, args, kwargs)
        instance.save()
        return self.get_serializer(instance)
