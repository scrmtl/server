from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import PlatformUser
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group


class ScrumUserCreationForm(UserCreationForm):

    class Meta:
        model = PlatformUser
        fields = ('username', 'email')


class ScrumUserChangeForm(UserChangeForm):

    class Meta:
        model = PlatformUser
        fields = UserChangeForm.Meta.fields


User = get_user_model()

# Create ModelForm based on the Group model.


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()
            print(self.fields['users'].initial)
            print(User.objects.all())

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance
