from django.contrib import admin
from .models import session_attendance, session_attended_options, group_membership, session_absent
from django.contrib.auth.models import Group

admin.site.site_header = 'Groups'

class session_attendanceAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'dateofvisit', 'session_attended', 'createdby', 'creation_date')

class session_attended_optionsAdmin(admin.ModelAdmin):
    list_display = ('session_attended', 'group_leader', 'creation_date')

class group_membershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'group', 'active')


class session_absentAdmin(admin.ModelAdmin):
    list_display = ('absentee', 'dateofmeeting',  'session_missed', 'follow_up_date', 'follow_up_Feedback')

# Register your models here.
admin.site.register(session_attendance, session_attendanceAdmin)
admin.site.register(session_attended_options, session_attended_optionsAdmin)
admin.site.register(group_membership, group_membershipAdmin)
admin.site.register(session_absent, session_absentAdmin)