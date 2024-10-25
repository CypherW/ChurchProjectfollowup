from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.group_attendance, name='group_attendance'),
    path('groups/update_attending_count', views.update_attending_count, name='update_attending_count'),
    path('groups/person/<int:pk>', views.group_person_detail, name='group_person_detail' ),
    path('groups/edit/<int:pk>', views.edit_person_details, name='edit_person_details' ),
    path('groups/addPerson', views.group_addPersonForm, name='addPersonForm' ),
    path('groups/check_person_exists', views.check_person_exists, name='check_person_exists' ),
    path('groups/present', views.present_bysession, name='present_bysession'),
    path('groups/load_session_members', views.load_session_members, name='load_session_members'),
    path('groups/load_searchByTyping_add_present', views.load_searchByTyping_add_present, name='load_searchByTyping_add_present'),
    path('groups/mark_attendee_present/<int:pk>', views.mark_attendee_present, name='mark_attendee_present'),
    path('groups/group_meetings', views.meeting_occurrences, name='meeting_occurrences'),
    path('groups/load_event_dates', views.load_event_dates, name='load_event_dates'),
    path('groups/load_event_date_attendance', views.load_event_date_attendance, name='load_event_date_attendance'),
    path('groups/load_dates_present_by_session', views.load_dates_present_by_session, name='load_dates_present_by_session'),
    path('groups/load_category_select_present_table', views.load_category_select_present_table, name='load_category_select_present_table'),
    path('groups/load_searchByTyping_attending', views.load_searchByTyping_attending, name='load_searchByTyping_attending'),
    path('groups/remove_attendee/<int:pk>', views.remove_attendee, name='remove_attendee'),
    path('groups/update_present_count', views.update_present_count, name='update_present_count'),
    path('groups/prayer_cell_check_present', views.prayer_cell_check_present, name='prayer_cell_check_present'),
    path('groups/prayer_cell_feedback_form/', views.prayer_cell_feedback_form, name='prayer_cell_feedback_form'),
    path('groups/feedback_form_already_submitted', views.prayer_cell_feedback_form, name='feedback_form_already_submitted'),
    path('groups/display_event_feedback_modal/', views.display_event_feedback_modal, name='display_event_feedback_modal'),
    path('groups/display_event_absent_modal/', views.display_event_absent_modal, name='display_event_absent_modal'),
    path('groups/display_absentee_feedback_modal/', views.display_absentee_feedback_modal, name='display_absentee_feedback_modal'),
    path('groups/display_event_present_modal/', views.display_event_present_modal, name='display_event_present_modal'),
    path('groups/redirect_display_event_feedback_modal/', views.redirect_display_event_feedback_modal, name='redirect_display_event_feedback_modal'),
    path('groups/add_toGroupForm/', views.add_toGroupForm, name='add_toGroupForm'),
    path('groups/isguardian_entered/', views.isguardian_entered, name='isguardian_entered'),
    path('groups/addPerson_Parent/<int:pk>', views.addPerson_Parent, name='addPerson_Parent'),
    path('groups/addPerson_existingParent/<int:pk>', views.addPerson_existingParent, name='addPerson_existingParent'),
    path('groups/addPerson_existingParent/load_searchByTyping_add_parent/', views.load_searchByTyping_add_parent, name='load_searchByTyping_add_parent'),
    path('groups/addPerson_existingParent/load_searchByTyping_add_parent_selectedParent', views.load_searchByTyping_add_parent_selectedParent, name='load_searchByTyping_add_parent_selectedParent'),
    path('groups/noFeedback_button', views.noFeedback_button, name='noFeedback_button'),
    path('groups/addPerson_existingParent/confirmed_exisiting_parent', views.confirmed_exisiting_parent, name='confirmed_exisiting_parent'),
    path('groups/group_absent_followup', views.group_absent_followup, name='group_absent_followup'),
    path('groups/multi_group_absent_followup_selected', views.multi_group_absent_followup_selected, name='multi_group_absent_followup_selected'),
    path('groups/multi_group_view_Previous_feedback_button', views.multi_group_view_Previous_feedback_button, name='multi_group_view_Previous_feedback_button'),
    path('groups/group_absentee_followup/<int:pk>', views.group_absentee_followup, name='group_absentee_followup'),
    path('groups/group_remove_member/<int:pk>', views.group_remove_member, name='group_remove_member'),
    path('groups/group_absent_view_feedback/<str:meeting>/', views.group_absent_view_feedback, name='group_absent_view_feedback'),
    path('groups/group_absentee_view_feedback/<int:pk>', views.group_absentee_view_feedback, name='group_absentee_view_feedback'),

]