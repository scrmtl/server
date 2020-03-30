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
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import json


class SteplistViewSet(viewsets.ModelViewSet):
    """Handels events that influence the whole list

    Parameters
    ----------

    """

    queryset = models.Steplist.objects.all()
    serializer_class = serializers.StepListSerializerCommon

    def retrieve(self, request, pk=None):
        """Gets you one steplist, with all steps included

        Returns
        -------
        json : Single steplist element with an array of steps
        """
        _steplist = get_object_or_404(self.queryset, pk=pk)
        _serializer_class = serializers.StepListSerializer(_steplist)

        return Response(_serializer_class.data)

    # def list(self, request):

    #     _list_serializer = self.serializer_class(self.queryset, many=True)
    #     json_dat = JSONRenderer().render(_list_serializer.data)
    #     print(json_dat)

    #     print(_list_serializer.data)

    #     return Response(_list_serializer.data)


# class Step(APIView):
#     """Handels events only effect one step

#     Parameters
#     ----------
#     APIView : APIView
#         Does not use HttpRequest and can handle POST, GET etc.
#     """

#     def get(self, request, format=None):
#         pass

#     def post(self, request, format=None):
#         """Processes the user input for adding a new element

#         Parameters
#         ----------
#         request : reqest
#             POST command in JSON format
#             {"text": string}

#         Returns
#         -------
#         JSON response
#             {"id": integer,
#             "text": string,
#             "checked": boolean,
#             "checklistName": string}
#         """
#         checklist_form = ChecklistForm(request.POST)
#         selected_checklist = ""
#         if (request.POST.get('checklistName') is None):
#             selected_checklist = models.Steplist.objects.get(
#                 name='Steplist 1')
#         # get the highest value in numbering
#         selected_checklist_items = models.SteplistItem.objects.filter(
#             Steplist=selected_checklist).order_by('-numbering'
#                                                    )[:1]
#         highest_number = selected_checklist_items[0].numbering

#         if checklist_form.is_valid():
#             checklist_item = models.SteplistItem(text=request.POST['text'])
#             checklist_item.Steplist = selected_checklist
#             checklist_item.checked = False
#             checklist_item.numbering = highest_number + 1
#             checklist_item.save()
#             checklist_item_json = json.dumps(
#                 {"id": checklist_item.id,
#                  "text": checklist_item.text,
#                  "checked": checklist_item.checked})
#             print(checklist_item_json)
#         return checklist_item_json

#     def delete(self, request, format=None):
#         """delete a Steplist item

#         Parameters
#         ----------
#         request : reqest
#             POST command in JSON format
#             {"id": integer}

#         Returns
#         -------
#         JSON response
#             {"id": integer}
#         """
#         item_id = request.POST.get('itemId')
#         checklist_item = models.SteplistItem.objects.get(pk=item_id)
#         checklist_item_json = json.dumps({"id": checklist_item.id})
#         checklist_item.delete()
#         print(checklist_item_json)
#         return checklist_item_json

#     def patch(self, request, format=None):
#         """Marks selected item as completed

#         Parameters
#         ----------
#         request : reqest
#             POST command in JSON format
#             {"itemId": integer,
#              "checked" : boolean,
#              "text" : string}

#         Returns
#         -------
#         JSON response
#             {"id": integer, "checked": boolean}
#         """
#         item_id = request.POST.get('itemId')
#         checklist_item = models.SteplistItem.objects.get(pk=item_id)
#         checklist_item.checked = not checklist_item.checked
#         checklist_item.save()
#         checklist_item_json = json.dumps({"id": checklist_item.id,
#                                           "checked": checklist_item.checked})
#         print(checklist_item_json)

#         """Processes the user input for changing the text of a task

#         Parameters
#         ----------
#         request : reqest
#             POST command in JSON format
#             {"itemId": integer, "text": string, "numbering": integer}

#         Returns
#         -------
#         JSON response
#             {"id": integer, "text": string, "numbering": integer}
#         """
#         item_id = request.POST.get('itemId')
#         item_text = request.POST.get('text')
#         item_numbering = request.POST.get('numbering')
#         checklist_item = models.SteplistItem.objects.get(pk=item_id)
#         if not (item_numbering is None):
#             new_item_number = int(item_numbering) - 1
#             selected_checklist = checklist_item.Steplist
#             print(selected_checklist.name)
#             print(checklist_item.Steplist.name)
#             selected_checklist_items = models.SteplistItem.objects.filter(
#                 Steplist=selected_checklist).order_by('numbering'
#                                                        ).exclude(pk=item_id)
#             for i, item in enumerate(selected_checklist_items):
#                 if ((item.numbering >= checklist_item.numbering) and
#                         (item.numbering <= new_item_number)):
#                     item.numbering = i
#                 elif ((item.numbering <= checklist_item.numbering) and
#                         (item.numbering >= new_item_number)):
#                     item.numbering = i + 1
#                 item.save()
#             checklist_item.numbering = int(item_numbering) - 1
#         checklist_item.text = item_text
#         checklist_item.save()
#         checklist_item_json = json.dumps(
#             {"id": checklist_item.id,
#              "text": checklist_item.text,
#              "numbering": checklist_item.numbering})
#         print(checklist_item_json)

#         return checklist_item_json
