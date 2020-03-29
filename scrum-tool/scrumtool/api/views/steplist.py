"""Controller methods in the app (MVC model)
"""
from django.shortcuts import render
# https://github.com/yceruto/django-ajax
from django_ajax.decorators import ajax

from scrumtoolHome import models
from scrumtoolHome.forms import ChecklistForm
from .. import serializers

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

import json


class SteplistViewSet(viewsets.ModelViewSet):
    """Handels events that influence the whole list

    Parameters
    ----------
    APIView : APIView
        Does not use HttpRequest and can handle POST, GET etc.
    """

    queryset = models.Checklist.object.all()
    serializer_class = serializers.Checklist

    def update(self, request, format=None))


class Step(APIView):
    """Handels events only effect one step

    Parameters
    ----------
    APIView : APIView
        Does not use HttpRequest and can handle POST, GET etc.
    """

    def get(self, request, format = None):
        pass

    def post(self, request, format = None):
        """Processes the user input for adding a new element

        Parameters
        ----------
        request : reqest
            POST command in JSON format
            {"text": string}

        Returns
        -------
        JSON response
            {"id": integer,
            "text": string,
            "checked": boolean,
            "checklistName": string}
        """
        checklist_form=ChecklistForm(request.POST)
        selected_checklist=""
        if (request.POST.get('checklistName') is None):
            selected_checklist=models.Checklist.objects.get(
                name = 'Checklist 1')
        # get the highest value in numbering
        selected_checklist_items=models.ChecklistItem.objects.filter(
            checklist=selected_checklist).order_by('-numbering'
                                                   )[:1]
        highest_number = selected_checklist_items[0].numbering

        if checklist_form.is_valid():
            checklist_item = models.ChecklistItem(text=request.POST['text'])
            checklist_item.checklist = selected_checklist
            checklist_item.checked = False
            checklist_item.numbering = highest_number + 1
            checklist_item.save()
            checklist_item_json = json.dumps(
                {"id": checklist_item.id,
                 "text": checklist_item.text,
                 "checked": checklist_item.checked})
            print(checklist_item_json)
        return checklist_item_json

    def delete(self, request, format=None):
        """delete a checklist item

        Parameters
        ----------
        request : reqest
            POST command in JSON format
            {"id": integer}

        Returns
        -------
        JSON response
            {"id": integer}
        """
        item_id = request.POST.get('itemId')
        checklist_item = models.ChecklistItem.objects.get(pk=item_id)
        checklist_item_json = json.dumps({"id": checklist_item.id})
        checklist_item.delete()
        print(checklist_item_json)
        return checklist_item_json

    def patch(self, request, format=None):
        """Marks selected item as completed

        Parameters
        ----------
        request : reqest
            POST command in JSON format
            {"itemId": integer,
             "checked" : boolean,
             "text" : string}

        Returns
        -------
        JSON response
            {"id": integer, "checked": boolean}
        """
        item_id = request.POST.get('itemId')
        checklist_item = models.ChecklistItem.objects.get(pk=item_id)
        checklist_item.checked = not checklist_item.checked
        checklist_item.save()
        checklist_item_json = json.dumps({"id": checklist_item.id,
                                          "checked": checklist_item.checked})
        print(checklist_item_json)

        """Processes the user input for changing the text of a task

        Parameters
        ----------
        request : reqest
            POST command in JSON format
            {"itemId": integer, "text": string, "numbering": integer}

        Returns
        -------
        JSON response
            {"id": integer, "text": string, "numbering": integer}
        """
        item_id = request.POST.get('itemId')
        item_text = request.POST.get('text')
        item_numbering = request.POST.get('numbering')
        checklist_item = models.ChecklistItem.objects.get(pk=item_id)
        if not (item_numbering is None):
            new_item_number = int(item_numbering) - 1
            selected_checklist = checklist_item.checklist
            print(selected_checklist.name)
            print(checklist_item.checklist.name)
            selected_checklist_items = models.ChecklistItem.objects.filter(
                checklist=selected_checklist).order_by('numbering'
                                                       ).exclude(pk=item_id)
            for i, item in enumerate(selected_checklist_items):
                if ((item.numbering >= checklist_item.numbering) and
                        (item.numbering <= new_item_number)):
                    item.numbering = i
                elif ((item.numbering <= checklist_item.numbering) and
                        (item.numbering >= new_item_number)):
                    item.numbering = i + 1
                item.save()
            checklist_item.numbering = int(item_numbering) - 1
        checklist_item.text = item_text
        checklist_item.save()
        checklist_item_json = json.dumps(
            {"id": checklist_item.id,
             "text": checklist_item.text,
             "numbering": checklist_item.numbering})
        print(checklist_item_json)

        return checklist_item_json
