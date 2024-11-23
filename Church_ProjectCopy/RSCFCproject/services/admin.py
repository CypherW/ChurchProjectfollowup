from django.contrib import admin
from .models import service_counts, childrensChurch_classes, childrensChurch_teachers, childrensChurch_class_member, class_attendance, class_service_feedback, transport_ministry, transport_passengers_list, trip_passengers, trip_passengers_absent

# Register your models here.

admin.site.site_header = 'Services'

class service_countsAdmin(admin.ModelAdmin):
    list_display = ('service_date', 'first_service_count', 'second_service_count')

class childrensChurch_classesAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'head_teacher')

class childrensChurch_teachersAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'get_classes')

    def get_classes(self, obj):
        return ",".join([classes.class_name for classes in obj.classes.all()])
    
    get_classes.short_description = 'Classes'

class childrensChurch_class_memberAdmin(admin.ModelAdmin):
    list_display = ('child', 'class_attending', 'active') 

class class_attendanceAdmin(admin.ModelAdmin):
    list_display = ('child', 'class_name', 'dateofclass', 'service') 


class transport_ministryAdmin(admin.ModelAdmin):
    list_display = ('passenger_assistant', 'area')
    
class transport_passengers_listAdmin(admin.ModelAdmin):
   list_display = ('passenger', 'bus_area', 'active')
    
class trip_passengersAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'area_from', 'dateoftrip', 'creation_date', 'created_by')

class trip_passengers_absentAdmin(admin.ModelAdmin):
    list_display = ('absentee', 'dateoftrip', 'transport_opp_missed', 'creation_date', 'follow_up_date', 'follow_up_Feedback')





# Register your models here.
admin.site.register(service_counts, service_countsAdmin)
admin.site.register(childrensChurch_classes, childrensChurch_classesAdmin)
admin.site.register(childrensChurch_teachers, childrensChurch_teachersAdmin)
admin.site.register(childrensChurch_class_member, childrensChurch_class_memberAdmin)
admin.site.register(class_attendance, class_attendanceAdmin)
admin.site.register(transport_ministry, transport_ministryAdmin)
admin.site.register(transport_passengers_list, transport_passengers_listAdmin)
admin.site.register(trip_passengers, trip_passengersAdmin)
admin.site.register(trip_passengers_absent, trip_passengers_absentAdmin)