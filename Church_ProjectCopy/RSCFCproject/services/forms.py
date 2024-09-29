from django import forms
from .models import service_counts

class service_count_form(forms.ModelForm):
    class Meta:
        model = service_counts
        fields = ['service_date', 'first_service_count', 'second_service_count']

        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 150px;', 'class': ''}),
        }