from django.contrib import admin
from .models import visit_details, visitor_first_followup, visitor_followup_call, visitor_referral_finalize
from django.contrib.auth.models import Group
admin.site.site_header = 'RSCFC Visitors'

class visit_detailsAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'dateofvisit', 'contactMethod')

class visitor_first_followupAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'method_of_followup', 'response', 'added_to_Whatsapp_group', 'followedup_up_by', 'date_of_followup')

class visitor_followup_callAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'general_feedback', 'prayer_request', 'date_of_followup', 'followedup_up_by')

class visitor_referral_finalizeAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'refer_to_church', 'refer_to_prayer_cell', 'finalize', 'date_of_followup', 'followedup_up_by')



# Register your models here.
admin.site.register(visit_details, visit_detailsAdmin)
admin.site.register(visitor_first_followup, visitor_first_followupAdmin)
admin.site.register(visitor_followup_call, visitor_followup_callAdmin)
admin.site.register(visitor_referral_finalize, visitor_referral_finalizeAdmin)
# admin.site.unregister(Group)

