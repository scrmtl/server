from django.urls import path
from .views import index, login


urlpatterns = [
        #wenn Anfrage reinkommt, dann übergebe das der Funktion index aus der views.py
        path ('', login, name='login.html'),
        path ('home', index, name='index.html')

]
