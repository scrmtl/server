""" Django’s built-in form support to make form processing easier
"""
from django import forms
from crispy_forms.utils import render_crispy_form


class ChecklistForm(forms.Form):
    """A HTML form for user input of Steplist elements
    """
    text = forms.CharField(
        max_length=256,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter todo e.g. Delete junk files',
                'aria-label': 'Todo',
                'aria-describedby': 'add-btn'}))
