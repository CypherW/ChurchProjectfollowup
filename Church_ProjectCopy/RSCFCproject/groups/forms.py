from django import forms
from people.models import People
from .models import session_attendance, session_attended_options, prayer_cell_feedback, session_absent, leaving_group
from datetime import date
from django.utils import timezone

class CustomDateInput(forms.DateInput):
    input_type = 'text'
    format = '%d %B %Y'

    def __init__(self, *args, **kwargs):
        kwargs['format'] = self.format
        super().__init__(*args, **kwargs)

    def format_value(self, value):
        if value:
            return value.strftime(self.format)
        return super().format_value(value)



class Person_Form(forms.ModelForm):
    class Meta:
        model = People
        fields = ['Name', 'Surname', 'CellNumber', 'EmailAddress', 'birthday', 'area', 'Gender']

        widgets = {
            'Name': forms.TextInput (attrs={'hx-get': 'check_person_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Surname'}),
            'Surname': forms.TextInput (attrs= {'hx-get': 'check_person_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Name'}),
            'birthday': forms.DateInput(format='%d %B %Y'),
        }
   
class Date_Attended_Form(forms.ModelForm):

    def __init__(self, group_leader_id, *args, **kwargs):
            super(Date_Attended_Form, self).__init__(*args, **kwargs)
            self.initial['dateofvisit'] = timezone.localtime().date()

             # Filter the queryset for the 'session_attended' field based on the group leader ID
            self.fields['session_attended'].queryset = session_attended_options.objects.filter(group_leader_id=group_leader_id)

    class Meta:
        model = session_attendance

        fields = ['session_attended', 'dateofvisit']

        widgets = {
            'dateofvisit': forms.DateInput(attrs={'hx-get': 'load_session_members', 'hx-target': '#attendance_table', 'hx-include': '#id_session_attended', 'type': 'date', 'style': 'width: 130px;', 'class': ''}),
            'session_attended': forms.Select(attrs={'hx-get': 'load_session_members', 'hx-target': '#attendance_table', 'hx-include': '#id_dateofvisit', 'class': 'm-1'})    
              }
       

class group_meetingsForm(forms.ModelForm):
    model = session_attendance
    fields = ['session_attended']

    session_attended = widget=forms.Select(attrs={'id': 'session'})

class group_type_select(forms.Form):
    session_attended_options = forms.ModelChoiceField(queryset=session_attended_options.objects.all(),
                                                      widget=forms.Select(attrs={"hx-get": "load_event_dates", "hx-target": "#meeting_listings", "class": 'm-2'}),
                                                    label='Group:'
    )
    
class present_select_fieldsForm(forms.Form):

    def __init__(self, group_leader_id, *args, **kwargs):
            super(present_select_fieldsForm, self).__init__(*args, **kwargs)
             # Filter the queryset for the 'session_attended' field based on the group leader ID
            self.fields['meeting_attended'].queryset = session_attended_options.objects.filter(group_leader_id=group_leader_id)

    meeting_attended = forms.ModelChoiceField(queryset=session_attended_options.objects.all(),
                                              widget=forms.Select(attrs={"hx-get": "load_dates_present_by_session", "hx-target": "#id_date", 'class': 'm-2'}))
    date = forms.ModelChoiceField(queryset=session_attendance.objects.none(),
                                  widget=forms.Select(attrs={"hx-get": "load_category_select_present_table", "hx-include": "#id_date, #id_meeting_attended", "hx-target": "#id_table", 'class': 'm-2'}))
    

class prayer_cell_feedbackForm(forms.ModelForm):
     
     word_discussed = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'small-textarea', 'rows': 2, 'cols': 40}),
        label='Word Discussed:'
    )
     prayed_about = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'small-textarea', 'rows': 2, 'cols': 40}),
        label='Prayed About:'
    )
     
     testimonies = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'class': 'small-textarea', 'rows': 2, 'cols': 40}),
        label='Testimonies:'
    )
     
     prayer_requests = forms.CharField(required=False,
         widget=forms.Textarea(attrs={'class': 'small-textarea', 'rows': 2, 'cols': 40}),
        label='Prayer Requests:'
     )
     class Meta:
        model = prayer_cell_feedback
        fields = ['word_discussed', 'prayed_about', 'testimonies', 'prayer_requests' ]

class absentee_followup_form(forms.ModelForm):

    follow_up_Feedback = forms.CharField(required=True,
         widget=forms.Textarea(attrs={'class': 'small-textarea mt-2', 'rows': 3, 'cols': 5}),
        label='Feedback:'
     )
    
    def __init__(self, *args, **kwargs):
            super(absentee_followup_form, self).__init__(*args, **kwargs)
            self.initial['follow_up_date'] = timezone.localtime().date()
            
    class Meta:

        model = session_absent
        fields = ['follow_up_Feedback', 'follow_up_date']

        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 150px; margin-right-3'}) 
              }
        

class remove_from_group_form(forms.ModelForm):

    reason_leaving = forms.CharField(required=True,
         widget=forms.Textarea(attrs={'class': 'small-textarea mt-2', 'rows': 3, 'cols': 5}),
        label='Reason Leaving Group:'
     )
    
    def __init__(self, *args, **kwargs):
            super(remove_from_group_form, self).__init__(*args, **kwargs)
            self.initial['follow_up_date'] = timezone.localtime().date()
            
    class Meta:

        model = leaving_group
        fields = ['reason_leaving', 'date_withdrew']

        widgets = {
            'date_withdrew': forms.DateInput(attrs={'type': 'date', 'style': 'width: 150px; margin-right-3'}) 
              }
        
        
        
class multiple_Group_absentee_feedback_form(forms.ModelForm):
    class Meta:
        model = session_attendance

        fields = ['session_attended']

        labels = {
            'session_attended': 'Select Group'
        }
 

        widgets = {
            'session_attended': forms.Select(attrs={'hx-get': 'multi_group_absent_followup_selected', 'hx-target': '#absent_table', 'hx-include': '#id_session_attended'})    
              }
        
        

    def __init__(self, group_leader_id, *args, **kwargs):
        super(multiple_Group_absentee_feedback_form, self).__init__(*args, **kwargs)
        # Filter the queryset for the 'session_attended' field based on the group leader ID
        self.fields['session_attended'].queryset = session_attended_options.objects.filter(group_leader_id=group_leader_id)