from django.urls import path
from .views import index


urlpatterns = [
        #wenn Anfrage reinkommt, dann übergebe das der Funktion index aus der views.py
        path ('', index, name='index'),

]
