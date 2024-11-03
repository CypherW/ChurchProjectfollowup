from django.contrib import admin
from .models import salvations, new_convert_first_followup, new_convert_followup_call, User, new_convert_referral_finalize
from django.contrib.auth.models import Group

admin.site.site_header = 'RSCFC New Converts'

class salvationsAdmin(admin.ModelAdmin):
    list_display = ('convert', 'dateofcommitment', 'contactMethod', 'decissionType')
    list_filter = ['convert']

class new_convert_first_followupAdmin(admin.ModelAdmin):
    list_display = ('convert', 'method_of_followup', 'response', 'added_to_Whatsapp_group', 'followedup_up_by', 'date_of_followup')
    list_filter = ['convert']

class new_convert_followup_callAdmin(admin.ModelAdmin):
    list_display = ('convert', 'general_feedback', 'prayer_request', 'date_of_followup', 'followedup_up_by')

class User(admin.ModelAdmin):
    list_display = ('staff')

class new_convert_referral_finalizeAdmin(admin.ModelAdmin):
    list_display = ('convert', 'refer_to_church', 'refer_to_prayer_cell', 'finalize', 'date_of_followup', 'followedup_up_by')



# Register your models here.
admin.site.register(salvations, salvationsAdmin)
admin.site.register(new_convert_first_followup, new_convert_first_followupAdmin)
admin.site.register(new_convert_followup_call, new_convert_followup_callAdmin)
admin.site.register(new_convert_referral_finalize, new_convert_referral_finalizeAdmin)
# admin.site.unregister(Group)