from django.urls import path
from . import views

urlpatterns= [
    path('visitors/add_new_visitor', views.add_new_visitor, name='add_new_visitor'),
    path('visitors/check_visitor_exists', views.check_visitor_exists, name='check_visitor_exists'),
    path('visitors/visitor_followup', views.visitor_followup, name='visitor_followup'),
    path('visitors/visitor_feedback/<int:pk>', views.visitor_feedback, name='visitor_feedback'),
    path('visitors/visitor_feedback/visitor_feedback_call/', views.visitor_feedback_call, name='visitor_feedback_call'),
    path('visitors/visitor_feedback/visitor_referral_finalize_view/', views.visitor_referral_finalize_view, name='visitor_referral_finalize_view'),



    ## OLD URLS - NEED TO BE REMOVED ####
    path('visitors/', views.visitors, name='visitors'),
    path('visitors/visitors-update/<int:pk>/', views.visitors_update, name='visitors-update'),
    path('visitors/visitors-delete/<int:pk>/', views.visitors_delete, name='visitors-delete'),
    path('visitors/visitors-update-existing/<int:pk>/', views.visitors_update_existing, name='visitors-update-existing'),
]