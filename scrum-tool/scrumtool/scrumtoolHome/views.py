from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .models import ProductBacklog, SprintBacklog, TaskCard, ChecklistItem, Checklist
from .forms import ChecklistForm


def index(request):
    # return HttpResponse("Hello World")
    context = {'backlog': ProductBacklog.objects.all(),
               'sb': SprintBacklog.objects.all(),
               'tasks': TaskCard.objects.all(),
               }

    return render(request=request, template_name='scrumtool/index.html',
                  context=context)


def login(request):

    return render(request=request, template_name='scrumtool/login.html')


def pb(request):
    context = {'backlog': ProductBacklog.objects.all(),
               }

    return render(request=request, template_name='scrumtool/pb.html',
                  context=context)


def sb(request):
    context = {'backlog': ProductBacklog.objects.all(),
               'sb': SprintBacklog.objects.all(),
               'tasks': TaskCard.objects.all(),
               }

    return render(request=request, template_name='scrumtool/sb.html',
                  context=context)


def checklist(request):
    checklistForm = ChecklistForm()
    context = {'checklistItems': ChecklistItem.objects.all(),
                'checklistForm': checklistForm
               }
    return render(request=request, template_name='scrumtool/checklist.html',
                  context=context)

@require_POST
def addChecklistItem(request):
    checklistForm = ChecklistForm(request.POST)

    if checklistForm.is_valid():
        newChecklistItem = ChecklistItem(name= request.POST['text'])
        newChecklistItem.checklist = Checklist.objects.get(id__exact=1)
        newChecklistItem.checked = False
        newChecklistItem.save()
    print(request.POST['text'])

    return redirect('http://localhost:8000/checklist')

def completeChecklistItem(request, itemId):

    checklistItem = ChecklistItem.objects.get(pk=itemId)
    checklistItem.checked = not checklistItem.checked
    checklistItem.save()

    return redirect('http://localhost:8000/checklist')

def deleteChecklistItem(request, itemId):
    ChecklistItem.objects.filter(id__exact=itemId).delete()
    return redirect('http://localhost:8000/checklist')