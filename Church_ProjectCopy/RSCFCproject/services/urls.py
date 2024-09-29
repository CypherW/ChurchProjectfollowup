from django.urls import path
from . import views

urlpatterns = [

    path('services/service_counts', views.service_countspage, name='service_counts'),
    path('services/stats', views.stats, name='stats'),
    
]
    