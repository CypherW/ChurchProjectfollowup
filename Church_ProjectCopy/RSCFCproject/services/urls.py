from django.urls import path
from . import views

urlpatterns = [

    path('services/service_counts', views.service_countspage, name='service_counts'),
    path('services/load_service_counts_by_date', views.load_service_counts_by_date, name='load_service_counts_by_date'),
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
    path('services/childrens_church_check_present', views.childrens_church_check_present, name='childrens_church_check_present'),
    path('services/remove_attendee_childrens_church/<int:pk>', views.remove_attendee_childrens_church, name='remove_attendee_childrens_church'),
    path('services/update_present_class_count', views.update_present_class_count, name='update_present_class_count'),
    path('services/passenger_check_in', views.passenger_check_in, name='passenger_check_in'),
    path('services/add_passenger', views.add_passenger, name='add_passenger'),
    path('services/check_passenger_exists', views.check_passenger_exists, name='check_passenger_exists'),
    path('services/load_passenger_members_list', views.load_passenger_members_list, name='load_passenger_members_list'),
    path('groups/mark_passenger_present/<int:pk>', views.mark_passenger_present, name='mark_passenger_present'),
    path('services/update_passenger_count', views.update_passenger_count, name='update_passenger_count'),
    path('services/load_searchByTyping_add_present_passenger', views.load_searchByTyping_add_present_passenger, name='load_searchByTyping_add_present_passenger'),
    path('services/transport_check_present', views.transport_check_present, name='transport_check_present'),
    path('services/remove_passenger/<int:pk>', views.remove_passenger, name='remove_passenger'),

    


    
]