"""Controller methods in the app (MVC model)
"""
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from rest_framework import permissions, status, mixins, generics
from api.views.nested_ressources_helper import NestedComponentViewSet, \
    NestedMtmMixin

from .. import models
from .. import serializers


class SteplistViewSet(AutoPermissionViewSetMixin,
                      NestedMtmMixin,
                      mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      NestedComponentViewSet):
    """Handels events that influence the whole list

    Parameters
    ----------

    """

    queryset = models.Steplist.objects.all()

    def get_queryset(self):
        if 'task_pk' not in self.kwargs:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(task=self.kwargs['task_pk'])
    serializer_class = serializers.StepListSerializerCommon

    def retrieve(self, request, pk=None):
        """Gets you one steplist, with all steps included

        Returns
        -------
        json : Single steplist element with an array of steps
        """
        steplist = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(steplist)

        return Response(serializer.data)


class StepViewSet(viewsets.ModelViewSet):
    """API for getting, changing and creating steps
    """
    queryset = models.SteplistItem.objects.all()

    def get_queryset(self):
        if 'steplist_pk' not in self.kwargs:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(steplist=self.kwargs['steplist_pk'])

    serializer_class = serializers.StepSerializer

    def update(self, request, steplist_pk=None, pk=None):
        """Update a step - automatically numbering will be changed
        for all elements in the list

        """
        _steplist_item = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(
            _steplist_item,
            data=request.data,
            context={'request': request},
            partial=True)
        serializer.is_valid(raise_exception=True)
        new_item_number = int(serializer.validated_data.get('numbering'))
        serializer.save()
        self.change_order(
            new_item_number=new_item_number,
            _steplist_item=_steplist_item)
        print(serializer.data)
        return Response(serializer.data)

    def change_order(self, new_item_number, _steplist_item):
        selected_checklist = _steplist_item.steplist
        selected_steplist_item = models.SteplistItem.objects.filter(
            steplist=selected_checklist).order_by(
                'numbering').exclude(pk=_steplist_item.id)
        for i, item in enumerate(selected_steplist_item):
            if ((item.numbering >= item.numbering) and
                    (item.numbering <= new_item_number)):
                item.numbering = i
            elif ((item.numbering <= item.numbering) and
                    (item.numbering >= new_item_number)):
                item.numbering = i + 1
            item.save()
