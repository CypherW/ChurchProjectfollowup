from django.contrib import admin
from .models import service_counts, childrensChurch_classes, childrensChurch_teachers, childrensChurch_class_member, class_attendance, class_service_feedback

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


# Register your models here.
admin.site.register(service_counts, service_countsAdmin)
admin.site.register(childrensChurch_classes, childrensChurch_classesAdmin)
admin.site.register(childrensChurch_teachers, childrensChurch_teachersAdmin)
admin.site.register(childrensChurch_class_member, childrensChurch_class_memberAdmin)
admin.site.register(class_attendance, class_attendanceAdmin)