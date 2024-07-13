import django_filters
from django_filters import FilterSet, DateFilter, CharFilter, OrderingFilter
from django import forms

from .models import session_attendance

class group_meetingsFilter(django_filters.FilterSet):
    
    class Meta:
        model = session_attendance
        fields = { 'session_attended': ['exact']}