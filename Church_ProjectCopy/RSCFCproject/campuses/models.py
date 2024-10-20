from django.db import models
from people.models import People
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


# Create your models here.

class campuses_details(models.Model):
    campus_leader = models.ForeignKey(User, models.CASCADE, null=False)
    campus_name = models.CharField(max_length=30, null=True, blank=True)
    campus_area = models.CharField(max_length=30, null=True, blank=True)
    overseer = models.ForeignKey(User, models.CASCADE, null=False, related_name='overseer')

    def __str__(self):
        return f'{self.campus_leader}'

class campus_meetings(models.Model):
    meeting_type = models.CharField(max_length=30, null=False, blank=False,  verbose_name= 'Service Type:')
    campus_leader =  models.ForeignKey(User, models.CASCADE, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    dateofmeeting = models.DateField(default=timezone.now, verbose_name = 'Date:')
    children_attending = models.CharField(max_length=8,null=True, blank=True)
    adults_attending = models.CharField(max_length=8,null=True, blank=True)
    salvations = models.CharField(max_length=8,null=True, blank=True)
    general_feedback = models.TextField(verbose_name='Feedback:', null=True, blank=True)

    def __str__(self):
        return f'{self.meeting_type}'
    


