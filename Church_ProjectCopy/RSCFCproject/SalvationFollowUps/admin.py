from django.contrib import admin
from .models import Converts, Followups, Requests_Feedback, User, Link_Church
from django.contrib.auth.models import Group

admin.site.site_header = 'RSCFC New Converts'

class ConvertsAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Surname', 'Gender', 'CellNumber', 'EmailAddress', 'whereConverted')
    list_filter = ['whereConverted', 'Gender']

class FollowupsAdmin(admin.ModelAdmin):
    list_display = ('convert', 'Language', 'AttendChurch')
    list_filter = ['AttendChurch']

class Requests_FeedbackAdmin(admin.ModelAdmin):
    list_display = ('convert', 'PrayerRequest', 'General')

class User(admin.ModelAdmin):
    list_display = ('staff')

class Link_ChurchAdmin(admin.ModelAdmin):
    list_display = ('convert', 'church_name')



# Register your models here.
admin.site.register(Converts, ConvertsAdmin)
admin.site.register(Followups, FollowupsAdmin)
admin.site.register(Requests_Feedback, Requests_FeedbackAdmin)
admin.site.register(Link_Church, Link_ChurchAdmin)
# admin.site.unregister(Group)