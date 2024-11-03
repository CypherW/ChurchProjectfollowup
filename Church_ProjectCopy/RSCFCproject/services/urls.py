from django.urls import path
from . import views

urlpatterns = [

    path('services/service_counts', views.service_countspage, name='service_counts'),
    path('services/stats', views.stats, name='stats'),
    path('services/childrens_church_attendance', views.childrens_church_attendance, name='childrens_church_attendance'),
    path('services/addPerson_childrens_church', views.addPerson_childrens_church, name='addPerson_childrens_church'),
    path('services/check_person_exists', views.check_person_exists, name='check_person_exists1'),
    path('services/isguardian_entered', views.isguardian_entered, name='isguardian_entered'),
    path('services/add_toClassForm', views.add_toClassForm, name='add_toClassForm'),
    path('services/addPerson_Parent/<int:pk>', views.addPerson_Parent, name='addPerson_Parent'),
    path('services/addPerson_Parent/check_parent_exists', views.check_parent_exists, name='check_parent_exists'),
    path('services/class_serviceComdinedOptions/<int:pk>', views.class_serviceComdinedOptions, name='class_serviceComdinedOptions'),
    path('services/load_class_members', views.load_class_members, name='load_class_members'),
    path('services/load_searchByTyping_add_present_learner', views.load_searchByTyping_add_present_learner, name='load_searchByTyping_add_present_learner'),
    path('groups/mark_child_present/<int:pk>', views.mark_child_present, name='mark_child_present'),
    path('groups/update_class_count', views.update_class_count, name='update_class_count'),


    
]