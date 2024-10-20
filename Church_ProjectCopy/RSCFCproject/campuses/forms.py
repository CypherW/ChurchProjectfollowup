from django import forms
from .models import campus_meetings
from django.utils import timezone



class campus_meeting_Form(forms.ModelForm):
     
     general_feedback = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'small-textarea', 'rows': 2, 'cols': 40}),
        label='General Feedback:'
    )
     class Meta:
        model = campus_meetings
        fields = ['dateofmeeting', 'meeting_type', 'adults_attending', 'children_attending', 'salvations', 'general_feedback']


        widgets = {
            'dateofmeeting': forms.DateInput(attrs={'type': 'date', 'style': 'width: 150px;', 'class': ''}),
        }