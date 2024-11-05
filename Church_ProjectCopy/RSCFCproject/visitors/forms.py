from django import forms
from django.forms.models import inlineformset_factory
from SalvationFollowUps.models import Converts, Requests_Feedback, Followups, Link_Church
from .models import visit_date, visit_details, visitor_first_followup, visitor_followup_call, visitor_referral_finalize
from people.models import People

class Person_Form(forms.ModelForm):
    class Meta:
        model = People
        fields = ['Name', 'Surname', 'CellNumber', 'EmailAddress', 'birthday', 'area', 'Gender']

        widgets = {
            'Name': forms.TextInput (attrs={'hx-get': 'check_visitor_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Surname'}),
            'Surname': forms.TextInput (attrs= {'hx-get': 'check_visitor_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Name'}),
            'birthday': forms.DateInput(format='%d %B %Y'),
        }

class visit_detailForm(forms.ModelForm):
    class Meta:
        model = visit_details
        fields = ['contactMethod', 'dateofvisit']

        widgets = {
            'dateofvisit': forms.DateInput(attrs={'type': 'date', 'style': 'width: 170px;', 'class': 'm-2'}),
            'contactMethod': forms.RadioSelect(attrs={'class': 'm-2'}),
            
              } 
              
        labels = {
            'contactMethod': 'How would you prefer to be reached?',
            'dateofvisit': 'Date of visit?'
        }

class visitor_First_FollowupForm(forms.ModelForm):
    class Meta:
        model = visitor_first_followup
        fields = ['method_of_followup', 'response', 'added_to_Whatsapp_group', 'date_of_followup']

        widgets = {
            'method_of_followup': forms.RadioSelect(attrs={'class': 'm-2'}),
            'response': forms.Textarea(attrs={'class': 'small-textarea', 'rows': 2, 'cols': 20, 'class': 'm-2'}),
            'added_to_Whatsapp_group': forms.RadioSelect(attrs={'class': 'm-2'}),
            'date_of_followup': forms.DateInput(attrs={'type': 'date', 'style': 'width: 170px;', 'class': 'm-2'}),
        }

        labels = {
                'method_of_followup': 'Followed up via:',
                'response:': 'test:',
                'added_to_Whatsapp_group': 'Added to Whatsapp group? (Brotherhood for men; You & Me for ladies)',
                'date_of_followup': 'Date of followup:',
            }

class visitor_Followup_call_Form(forms.ModelForm):
    class Meta:
        model = visitor_followup_call
        fields = ['general_feedback', 'prayer_request', 'date_of_followup']

        widgets = {
            'general_feedback': forms.Textarea(attrs={'class': 'small-textarea', 'rows': 2, 'cols': 20, 'class': 'm-2'}),
            'prayer_request': forms.Textarea(attrs={'class': 'small-textarea', 'rows': 2, 'cols': 20, 'class': 'm-2'}),
            'date_of_followup': forms.DateInput(attrs={'type': 'date', 'style': 'width: 170px;', 'class': 'm-2'}),
              } 

        labels = {
            'general_feedback': 'General Feedback:',
            'prayer_request:': 'Prayer Request:',
            'date_of_followup': 'Date of call:'
        }

class visitor_referral_finalize_form(forms.ModelForm):
    class Meta:
        model = visitor_referral_finalize
        fields = ['refer_to_church', 'refer_to_prayer_cell', 'refer_to_campus', 'finalize', 'date_of_followup']

        widgets = {
            'refer_to_church': forms.TextInput(),
            'prayer_request': forms.Textarea(attrs={'class': 'small-textarea', 'rows': 2, 'cols': 20, 'class': 'm-2'}),
            'refer_to_prayer_cell': forms.Select(attrs={'class': 'm-1'}),
            'refer_to_campus': forms.Select(attrs={'class': 'm-1'}),
            'date_of_followup': forms.DateInput(attrs={'type': 'date', 'style': 'width: 170px;', 'class': 'm-2'}),
                } 

        labels = {
            'refer_to_church': 'If referred to another church please input the name of the church?',
            'refer_to_prayer_cell:': 'Refer to prayer cell:',
            'refer_to_campus': 'Refer to campus:',
            'finalize': 'Click to mark as finalized:',
            'date_of_followup': 'Date:',
        }


##### OLD FORMS - NEED TO BE REMOVED ###
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