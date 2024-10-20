from django.urls import path
from . import views

urlpatterns = [
    path('campuses/campus_meetings', views.campus_meetings_feedback, name='campus_meetings'),
    path('campuses/view_campus_feedback', views.view_campus_feedback, name='view_campus_feedback'),
    

]