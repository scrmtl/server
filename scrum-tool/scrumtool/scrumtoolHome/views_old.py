"""Controller methods in the app (MVC model)
"""
from django.shortcuts import render
# https://github.com/yceruto/django-ajax
from django_ajax.decorators import ajax

from . import models
from .forms import ChecklistForm
from api.serializers import step_serializer, steplist_serializer
from rest_framework.renderers import JSONRenderer
import json


def index(request):
    """Shows index.html website

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.

    Returns
    -------
    HttpResponse
        Answer element according to the request
    """
    context = {'backlog': models.ProductBacklog.objects.all(),
               'sb': models.SprintBacklog.objects.all(),
               'tasks': models.TaskCard.objects.all(),
               }

    return render(request=request, template_name='scrumtool/index.html',
                  context=context)


def login(request):
    """Shows login.html website

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.

    Returns
    -------
    HttpResponse
        Answer element according to the request
    """
    return render(request=request, template_name='scrumtool/login.html')


def pb(request):
    """Shows the selected product backlog

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.

    Returns
    -------
    HttpResponse
        Answer element according to the request
    """
    context = {'backlog': models.ProductBacklog.objects.all(),
               }

    return render(request=request, template_name='scrumtool/pb.html',
                  context=context)


def sb(request):
    """Shows the selected sprint backlog

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.

    Returns
    -------
    HttpResponse
        Answer element according to the request
    """
    context = {'backlog': models.ProductBacklog.objects.all(),
               'sb': models.SprintBacklog.objects.all(),
               'tasks': models.TaskCard.objects.all(),
               }

    return render(request=request, template_name='scrumtool/sb.html',
                  context=context)


def Steplist(request):
    """Shows a Steplist with items

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.

    Returns
    -------
    HttpResponse
        Answer element according to the request
    """
    checklist_form = ChecklistForm()
    # TODO:
    selected_checklist = models.Steplist.objects.get(name='Checklist 1')
    selected_checklist_items = models.SteplistItem.objects.filter(
        Steplist=selected_checklist).order_by('numbering')
    context = {'checklistItems': selected_checklist_items,
               'checklistForm': checklist_form
               }
    return render(request=request, template_name='scrumtool/Steplist.html',
                  context=context)


"""
The following methods are using https://github.com/yceruto/django-ajax

They always return data in the following jason format:
{"status": 200, "statusText": "OK", "content ": xxx}
whereby the content is again in JSON format.
The content is specified separately for each function.
"""
@ajax
def delete_checklist_item(request):
    """delete a Steplist item

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
    checklist_item = models.SteplistItem.objects.get(pk=item_id)
    checklist_item_json = json.dumps({"id": checklist_item.id})
    checklist_item.delete()
    print(checklist_item_json)
    return checklist_item_json


@ajax
def complete_checklist_item(request):
    """Marks selected item as completed

    Parameters
    ----------
    request : reqest
        POST command in JSON format
        {"itemId": integer}

    Returns
    -------
    JSON response
        {"id": integer, "checked": boolean}
    """
    item_id = request.POST.get('itemId')
    checklist_item = models.SteplistItem.objects.get(pk=item_id)
    checklist_item.checked = not checklist_item.checked
    checklist_item.save()
    checklist_item_json = json.dumps({"id": checklist_item.id,
                                      "checked": checklist_item.checked})
    print(checklist_item_json)
    return checklist_item_json


@ajax
def add_checklist_item(request):
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
    checklist_form = ChecklistForm(request.POST)
    selected_checklist = ""
    if (request.POST.get('checklistName') is None):
        selected_checklist = models.Steplist.objects.get(name='Steplist 1')
    # get the highest value in numbering
    selected_checklist_items = models.SteplistItem.objects.filter(
        Steplist=selected_checklist).order_by('-numbering'
                                              )[:1]
    highest_number = selected_checklist_items[0].numbering

    if checklist_form.is_valid():
        checklist_item = models.SteplistItem(text=request.POST['text'])
        checklist_item.Steplist = selected_checklist
        checklist_item.checked = False
        checklist_item.numbering = highest_number + 1
        checklist_item.save()
        checklist_item_json = json.dumps({"id": checklist_item.id,
                                          "text": checklist_item.text,
                                          "checked": checklist_item.checked})
        print(checklist_item_json)
        return checklist_item_json


@ajax
def change_checklist_item(request):
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
    checklist_item = models.SteplistItem.objects.get(pk=item_id)
    checklist_list = models.Steplist.objects.get(
        SteplistItem=checklist_item)

    _step_serializer = step_serializer.StepSerializer(
        checklist_item)
    json_dat = JSONRenderer().render(_step_serializer.data)
    print(json_dat)
    _list_serializer = steplist_serializer.StepListSerializer(
        checklist_list)
    json_dat = JSONRenderer().render(_list_serializer.data)
    print(json_dat)

    if not (item_numbering is None):
        new_item_number = int(item_numbering) - 1
        selected_checklist = checklist_item.Steplist
        print(selected_checklist.name)
        print(checklist_item.Steplist.name)
        selected_checklist_items = models.SteplistItem.objects.filter(
            Steplist=selected_checklist).order_by('numbering'
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
    checklist_item_json = json.dumps({"id": checklist_item.id,
                                      "text": checklist_item.text,
                                      "numbering": checklist_item.numbering})
    print(checklist_item_json)
    return checklist_item_json
