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
    path('addChecklistItem', views.addChecklistItem, name='addChecklistItem'),
    path('completeChecklistItem/<itemId>',
         views.completeChecklistItem, name='completeChecklistItem'),
    path('deleteChecklistItem/<itemId>',
         views.deleteChecklistItem, name='deleteChecklistItem')
]
