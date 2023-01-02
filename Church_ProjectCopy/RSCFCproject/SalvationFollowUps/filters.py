import django_filters

from .models import Converts

class ConvertsFilter(django_filters.FilterSet):

    class Meta:
        model = Converts
        fields = {'Gender': ['exact'], 'whereConverted': ['exact']}