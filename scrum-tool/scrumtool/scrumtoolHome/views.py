"""Controller methods in the app (MVC model)
"""
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django_ajax.decorators import ajax

from . import models
from .forms import ChecklistForm

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


def checklist(request):
    """Shows a checklist with items

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.

    Returns
    -------
    HttpResponse
        Answer element according to the request
    """
    checklistForm = ChecklistForm()
    context = {'checklistItems': models.ChecklistItem.objects.all(),
               'checklistForm': checklistForm
               }
    return render(request=request, template_name='scrumtool/checklist.html',
                  context=context)


@require_POST
def addChecklistItem(request):
    """Processes the user input for adding a new element

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.

    Returns
    -------
    HttpResponseRedirect
        Redirect to a specific page
    """
    checklistForm = ChecklistForm(request.POST)

    if checklistForm.is_valid():
        newChecklistItem = models.ChecklistItem(name=request.POST['text'])
        newChecklistItem.checklist = models.Checklist.objects.get(id__exact=1)
        newChecklistItem.checked = False
        newChecklistItem.save()
    print(request.POST['text'])

    return redirect('http://localhost:8000/checklist')


def completeChecklistItem(request, itemId):
    """Marks selected item as completed

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.
    itemId : integer
        Id of the checklist item.

    Returns
    -------
    HttpResponseRedirect
        Redirect to a specific page
    """
    checklistItem = models.ChecklistItem.objects.get(pk=itemId)
    checklistItem.checked = not checklistItem.checked
    checklistItem.save()

    return redirect('http://localhost:8000/checklist')


def deleteChecklistItem(request, itemId):
    """Delete selected item as completed

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.
    itemId : integer
        Id of the checklist item.

    Returns
    -------
    HttpResponseRedirect
        Redirect to a specific page
    """
    models.ChecklistItem.objects.filter(id__exact=itemId).delete()
    return redirect('http://localhost:8000/checklist')


@ajax
def delete_checklist_item(request):
    """delete a checklist item

    Parameters
    ----------
    request : reqest
        POST command
    """
    item_id = request.POST.get('itemId')
    checklist_item = models.ChecklistItem.objects.get(pk=item_id)
    checklist_item_json = json.dumps({"id": checklist_item.id})
    checklist_item.delete()
    print(checklist_item_json)
    return checklist_item_json


@ajax
def complete_checklist_item(request):
    """Marks selected item as completed

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.
    itemId : integer
        Id of the checklist item.

    Returns
    -------
    HttpResponseRedirect
        Redirect to a specific page
    """
    item_id = request.POST.get('itemId')
    checklist_item = models.ChecklistItem.objects.get(pk=item_id)
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
    request : HttpRequest
        The request object used to generate this response.

    Returns
    -------
    HttpResponseRedirect
        Redirect to a specific page
    """
    checklist_form = ChecklistForm(request.POST)

    if checklist_form.is_valid():
        checklist_item = models.ChecklistItem(name=request.POST['text'])
        checklist_item.checklist = models.Checklist.objects.get(id__exact=1)
        checklist_item.checked = False
        checklist_item.save()
        checklist_item_json = json.dumps({"id": checklist_item.id,
                                          "name": checklist_item.name,
                                          "checked": checklist_item.checked})
        print(checklist_item_json)
        return checklist_item_json


@ajax
def change_checklist_item(request):
    """Processes the user input for adding a new element

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate this response.

    Returns
    -------
    HttpResponseRedirect
        Redirect to a specific page
    """
    item_id = request.POST.get('itemId')
    item_name = request.POST.get('name')
    checklist_item = models.ChecklistItem.objects.get(pk=item_id)
    checklist_item.name = item_name
    checklist_item.save()
    checklist_item_json = json.dumps({"id": checklist_item.id,
                                      "name": checklist_item.name})
    print(checklist_item_json)
    return checklist_item_json
