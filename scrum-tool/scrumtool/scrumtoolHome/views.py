from django.shortcuts import render
from django.http import HttpResponse
from .models import ProductBacklog, SprintBacklog, TaskCard, adminUser, normalUser

def index(request):
    #return HttpResponse("Hello World")
    context = {'backlog': ProductBacklog.objects.all(),
                'sb': SprintBacklog.objects.all(),
                'tasks': TaskCard.objects.all(),
                'adminUser': adminUser.objects.all(),
                'normalUser': normalUser.objects.all()
                }

    return render(request=request, template_name='scrumtool/index.html',
                    context=context)


def login(request):
    context= {'adminUser': adminUser.objects.all(),
                'normalUser': normalUser.objects.all()
                }
    
    return render(request=request, template_name='scrumtool/login.html')

