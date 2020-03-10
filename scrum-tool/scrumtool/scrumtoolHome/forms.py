from django import forms

class ChecklistForm(forms.Form):
    text = forms.CharField(max_length=256,
            widget=forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Enter todo e.g. Delete junk files',
                    'aria-label' : 'Todo',
                    'aria-describedby' : 'add-btn'
                }
            ))
