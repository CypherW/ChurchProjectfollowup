from django import forms
from .models import Converts, Requests_Feedback, Followups, Link_Church

class ConvertsForm(forms.ModelForm):
    class Meta:
        model = Converts
        fields = ['Name', 'Surname', 'Gender', 'CellNumber', 'EmailAddress', 'whereConverted', 'area']
            


class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = Requests_Feedback
        fields = ['convert', 'PrayerRequest', 'General']

class FollowupForm(forms.ModelForm):
    class Meta:
        model = Followups
        fields = ['Language', 'AttendChurch', 'next_followUpdate']
        widgets = {
            'next_followUpdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

class LinkchurchForm(forms.ModelForm):
    class Meta:
        model = Link_Church
        fields = ['church_name']