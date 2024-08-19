from django import forms
from .models import Converts, Requests_Feedback, Followups, Link_Church, salvations

class convertForm(forms.ModelForm):
    class Meta:
        model = salvations
        fields = ['contactMethod', 'decissionType', 'dateofcommitment']

        widgets = {
            'contactMethod': forms.RadioSelect(attrs={'class': 'm-2'}),
            'decissionType': forms.RadioSelect(attrs={'class': 'm-2'}),
            'dateofcommitment': forms.DateInput(attrs={'type': 'date', 'style': 'width: 170px;', 'class': 'm-2'}),
              } 
              
        labels = {
            'contactMethod': 'How would you prefer to be reached?',
            'decissionType': 'Is this your first time accepting Jesus as Saviour?',
            'dateofcommitment': 'Date of decission?'
        }

#### OLD FORMS NEED TO BE REMOVED

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