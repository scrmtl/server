"""Entry point for Django urls is the scrumtoolHome app
"""
from django.urls import path
from . import views_old


urlpatterns = [
    # When a request comes in, then pass it to the index function from views.py
    path('', views_old.login, name='login.html'),
    path('home', views_old.index, name='index.html'),
    path('pb', views_old.pb, name='pb.html'),
    path('sb', views_old.sb, name='sb.html'),
    path('Steplist', views_old.Steplist, name='Steplist.html'),
    path('delete_checklist_item', views_old.delete_checklist_item,
         name='delete_checklist_item'),
    path('add_checklist_item', views_old.add_checklist_item,
         name='add_checklist_item'),
    path('complete_checklist_item', views_old.complete_checklist_item,
         name='complete_checklist_item'),
    path('change_checklist_item', views_old.change_checklist_item,
         name='change_checklist_item')
]
