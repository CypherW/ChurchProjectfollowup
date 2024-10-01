from django.urls import path
from . import views

urlpatterns = [

    path('salvations/add_new_convert', views.add_new_convert, name='add_new_convert'),
    path('salvations/new_convert_followup', views.new_convert_followup, name='new_convert_followup'),
    path('salvations/new_Convert_feedback/<int:pk>', views.new_Convert_feedback, name='new_Convert_feedback'),
    path('salvations/new_Convert_feedback/new_Convert_feedback_call/', views.new_Convert_feedback_call, name='new_Convert_feedback_call'),
    path('salvations/new_Convert_feedback/new_convert_referral_finalize/', views.new_convert_referral_finalize, name='new_convert_referral_finalize'),

    #### OLD URLS NEED TO BE REMOVED
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/detail/<int:pk>', views.staff_detail, name='dashboard-staff-detail'),
    path('salvations/delete/<int:pk>/', views.converts_delete, name='dashboard-salvations-delete'),
    path('salvations/update/<int:pk>/', views.converts_update, name='dashboard-salvations-update'),
    path('followup_due/', views.Followup_due, name='dashboard-followup_due'),
    path('followup/<int:pk>/', views.followup, name='dashboard-followup'),
    path('church-connect/', views.church_connect, name='dashboard-church-connect'),
    path('church-connect-link/<int:pk>/', views.church_connect_link, name='dashboard-church-connect-link'),
]