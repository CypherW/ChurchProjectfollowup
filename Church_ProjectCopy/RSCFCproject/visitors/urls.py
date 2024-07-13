from django.urls import path
from . import views

urlpatterns= [
    path('visitors/', views.visitors, name='visitors'),
    path('visitors/visitors-update/<int:pk>/', views.visitors_update, name='visitors-update'),
    path('visitors/visitors-delete/<int:pk>/', views.visitors_delete, name='visitors-delete'),
    path('visitors/visitors-update-existing/<int:pk>/', views.visitors_update_existing, name='visitors-update-existing'),
]