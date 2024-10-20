from django.contrib import admin
from .models import campuses_details, campus_meetings
from django.contrib.auth.models import Group

admin.site.site_header = 'campuses_details'

class campuses_detailsAdmin(admin.ModelAdmin):
    list_display = ('campus_leader', 'campus_name', 'campus_area', 'overseer')

class campus_meetingsAdmin(admin.ModelAdmin):
    list_display = ('meeting_type', 'campus_leader', 'creation_date', 'dateofmeeting', 'children_attending', 'adults_attending', 'salvations', 'general_feedback')



# Register your models here.
admin.site.register(campuses_details, campuses_detailsAdmin)
admin.site.register(campus_meetings, campus_meetingsAdmin)