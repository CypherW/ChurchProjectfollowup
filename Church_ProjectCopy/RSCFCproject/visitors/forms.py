from django import forms
from django.forms.models import inlineformset_factory
from SalvationFollowUps.models import Converts, Requests_Feedback, Followups, Link_Church
from .models import visit_date

class ConvertsForm(forms.ModelForm):
    class Meta:
        model = Converts
        fields = ['Name', 'Surname', 'Gender', 'CellNumber', 'EmailAddress', 'area']


visit_dateInlineFormset = inlineformset_factory(Converts, visit_date, fields=['dateofvisit'], extra=1, can_delete=False, widgets = {
            'dateofvisit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})})

class visitorFollowupForm(forms.ModelForm):
    class Meta:
        model = Followups
        fields = ['Language', 'AttendChurch', 'next_followUpdate']
        widgets = {
            'next_followUpdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

class visit_date_existingPersonForm(forms.ModelForm):

    class Meta:
        model = Converts
        fields = ['Gender', 'CellNumber', 'EmailAddress', 'area']


visit_dateInlineFormset = inlineformset_factory(Converts, visit_date, fields=['dateofvisit'], extra=1, can_delete=False, widgets = {
            'dateofvisit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})})