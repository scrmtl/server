"""Controller methods in the app (MVC model)
"""
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from . import models
from .forms import ChecklistForm


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
