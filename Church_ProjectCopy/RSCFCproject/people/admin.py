from django.contrib import admin
from .models import People

admin.site.site_header = 'People'

class PeopleAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Surname', 'Gender', 'CellNumber', 'EmailAddress','EmailAddress', 'birthday', 'area', 'createdBy', 'creation_date')




# Register your models here.
admin.site.register(People, PeopleAdmin)