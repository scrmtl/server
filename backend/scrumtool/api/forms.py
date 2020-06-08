from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ScrumUser


class ScrumUserCreationForm(UserCreationForm):

    class Meta:
        model = ScrumUser
        fields = ('username', 'email')


class ScrumUserChangeForm(UserChangeForm):

    class Meta:
        model = ScrumUser
        fields = UserChangeForm.Meta.fields
