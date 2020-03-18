"""Entry point for Django urls is the scrumtoolHome app
"""
from django.urls import path
from . import views


urlpatterns = [
    # When a request comes in, then pass it to the index function from views.py
    path('', views.login, name='login.html'),
    path('home', views.index, name='index.html'),
    path('pb', views.pb, name='pb.html'),
    path('sb', views.sb, name='sb.html'),
    path('checklist', views.checklist, name='checklist.html'),
    path('delete_checklist_item', views.delete_checklist_item,
         name='delete_checklist_item'),
    path('add_checklist_item', views.add_checklist_item,
         name='add_checklist_item'),
    path('complete_checklist_item', views.complete_checklist_item,
         name='complete_checklist_item'),
    path('change_checklist_item', views.change_checklist_item,
         name='change_checklist_item')
]
