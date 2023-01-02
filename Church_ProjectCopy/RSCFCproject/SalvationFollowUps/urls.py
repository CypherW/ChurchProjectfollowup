from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/detail/<int:pk>', views.staff_detail, name='dashboard-staff-detail'),
    path('salvations/', views.salvations, name='dashboard-salvations'),
    path('salvations/delete/<int:pk>/', views.converts_delete, name='dashboard-salvations-delete'),
    path('salvations/update/<int:pk>/', views.converts_update, name='dashboard-salvations-update'),
    path('followup_due/', views.Followup_due, name='dashboard-followup_due'),
    path('followup/<int:pk>/', views.followup, name='dashboard-followup'),
    path('church-connect/', views.church_connect, name='dashboard-church-connect'),
    path('church-connect-link/<int:pk>/', views.church_connect_link, name='dashboard-church-connect-link'),
]