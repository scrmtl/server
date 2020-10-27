"""Helper for nested ressources like Tasks/1/?Label=1
Only Provides Create and delete
    """

import logging
from rest_framework.request import Request
from rest_framework import generics, viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import FieldError

from api.models.lane import LaneFilterSet, Lane

logger = logging.getLogger(__name__)


class NestedMtmMixin(mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    A mixin that provides default `partial_update()`, `destroy() actions.
    """
    allowed_attr = []

    def partial_update(self, request: Request, *args, **kwargs):
        """Adds an element to the specified many to many relation

        Parameters
        ----------
        request : Request
            Has to provide items in query_params (key, value)

        example:
            tasks/1/?labels=1

        """
        instance = self.get_object()
        try:
            for key, value in request.query_params.items():
                attr = self._get_mtm_attribute(key=key, instance=instance)
                attr.add(value)
            instance.save()
        except ValueError as error:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=str(error))

        if not request.query_params.dict():
            return super().partial_update(request, args, kwargs)
        return Response(self.get_serializer(instance).data)

    def destroy(self, request: Request, *args, **kwargs):
        """Adds an element to the specified many to many relation

        Parameters
        ----------
        request : Request
            Has to provide items in query_params (key, value)

        example:
        ---> tasks/1/?labels=1

        """
        instance = self.get_object()
        try:
            for key, value in request.query_params.items():
                attr = self._get_mtm_attribute(key=key, instance=instance)
                attr.remove(value)
            instance.save()
        except ValueError as error:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=str(error))
        if not request.query_params.dict():
            return super().destroy(request, args, kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_mtm_attribute(self, key, instance):
        error_msg = ""
        if hasattr(instance, key):
            attr = getattr(instance, key)
            attr_type = instance._meta.get_field(key).get_internal_type()
            # Only ManyToManyFields are allowd.
            if(attr_type == 'ManyToManyField'):
                # If allowed_attr is defined check if it contains key
                if not self.allowed_attr or (key in self.allowed_attr):
                    return attr
                else:
                    error_msg = (
                        "Access to attribute '%s' is permitted" %
                        key)
            else:
                error_msg = (
                    "An attribute '%s' that is not a many to many"
                    "relation but of type '%s' was tried to manipulate"
                    % (key, attr_type))
        else:
            error_msg = (
                "An attribute '%s' that is not a member of %s"
                "was tried to manipulate"
                % (key, instance))
        logger.warning(error_msg)
        raise ValueError(error_msg)


class NestedComponentViewSet(viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        model = self.get_serializer().Meta.model
        filter_params: Q = None
        for key, value in self.request.query_params.items():
            if hasattr(model, key):
                q = Q(**{"%s__id" % key: value})
                if filter_params:
                    filter_params = filter_params & q
                else:
                    filter_params = q
        try:
            if filter_params:
                queryset = queryset.filter(filter_params)
        except FieldError as err:
            logger.info("Parameter is not an model attribute: ")
        return queryset


def filter_queryset_by_query_params(function):
    def wrapper(*args, **kwargs):
        queryset = super().get_queryset()
        filter_params: Q = None
        for key, value in args[0].request.query_params.items():
            q = Q(**{"%s__id" % key: value})
            if filter_params:
                filter_params = filter_params & q
            else:
                filter_params = q
            args[0].queryset = queryset.filter(filter_params)
            queryset = args[0].function()
            print(args[0].queryset)
            print(queryset)
            return queryset
    return wrapper
