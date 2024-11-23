from django import forms
from .models import service_counts, class_attendance, childrensChurch_classes, trip_passengers
from people.models import People
from django.utils import timezone

class service_count_form(forms.ModelForm):
    class Meta:
        model = service_counts
        fields = ['service_date', 'first_service_count', 'second_service_count']

        widgets = {
            'service_date': forms.DateInput(attrs={'hx-get': 'load_service_counts_by_date', 'hx-target': '#counts_form', 'hx-trigger': 'change', 'hx-swap':'outerHTML', 'type': 'date', 'style': 'width: 150px;', 'class': ''}),
        }

class Person_Form(forms.ModelForm):
    class Meta:
        model = People
        fields = ['Name', 'Surname', 'CellNumber', 'EmailAddress', 'birthday', 'area', 'Gender']

        widgets = {
            'Name': forms.TextInput (attrs={'hx-get': 'check_person_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Surname'}),
            'Surname': forms.TextInput (attrs= {'hx-get': 'check_person_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Name'}),
            'birthday': forms.DateInput(format='%d %B %Y'),
        }

class Parent_Form(forms.ModelForm):
    class Meta:
        model = People
        fields = ['Name', 'Surname', 'CellNumber', 'EmailAddress', 'birthday', 'area', 'Gender']

        widgets = {
            'Name': forms.TextInput (attrs={'hx-get': 'check_parent_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Surname, #child'}),
            'Surname': forms.TextInput (attrs= {'hx-get': 'check_parent_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Name, #child'}),
            'birthday': forms.DateInput(format='%d %B %Y'),
        }

class childrensChurchAttendanceForm(forms.Form):

    def __init__(self, group_leader_id, *args, **kwargs):
            super(childrensChurchAttendanceForm, self).__init__(*args, **kwargs)
            self.initial['date'] = timezone.localtime().date()
            
    class_attending = forms.ModelChoiceField(queryset=childrensChurch_classes.objects.none(),
                                  widget=forms.Select(attrs={"hx-get": "load_class_members", "hx-include": "#id_date, #id_class_attending", "hx-target": "#attendance_table", 'class': 'm-2'}),
                                  label='Class'
    )
    
   
    date = forms.DateField(widget=forms.DateInput(attrs={'hx-get': 'load_class_members', 'hx-target': '#attendance_table', 'hx-include': '#id_class_attending', 'type': 'date', 'style': 'width: 130px;', 'class': 'm-2'}))
    
    
class add_Passenger_Form(forms.ModelForm):
    class Meta:
        model = People
        fields = ['Name', 'Surname', 'CellNumber', 'EmailAddress', 'birthday', 'area', 'Gender']

        widgets = {
            'Name': forms.TextInput (attrs={'hx-get': 'check_passenger_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Surname'}),
            'Surname': forms.TextInput (attrs= {'hx-get': 'check_passenger_exists', 'hx-target': '#modal-here', 'hx-trigger': 'keyup changed delay:900ms', 'hx-include': '#id_Name'}),
            'birthday': forms.DateInput(format='%d %B %Y'),
        }

class transport_AttendanceForm(forms.Form):

    def __init__(self, *args, **kwargs):
            super(transport_AttendanceForm, self).__init__(*args, **kwargs)
            self.initial['dateoftrip'] = timezone.localtime().date()

    model = trip_passengers
    fields = ['dateoftrip'
              ]
    
   
    dateoftrip = forms.DateField(widget=forms.DateInput(attrs={'hx-get': 'load_passenger_members_list', 'hx-target': '#attendance_table', 'hx-include': '#id_dateoftrip', 'type': 'date', 'style': 'width: 130px;', 'class': 'm-2'}), 
                                 label='Date:'
                                 )