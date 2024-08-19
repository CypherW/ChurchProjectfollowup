from django import forms
from .models import People


class Person_Form(forms.ModelForm):
    class Meta:
        model = People
        fields = ['Name', 'Surname', 'CellNumber', 'EmailAddress', 'birthday', 'area', 'Gender']
