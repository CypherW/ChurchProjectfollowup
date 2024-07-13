from django.db import models
from people.models import People
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

session_attended = (
    ('1', 'FaithKids 1st Service'),
    ('2', 'FaithKids 2nd Service'),
    ('3', 'Big Church 1st Service'),
    ('4', 'Big Church 2nd Service'),
    ('5', 'Ylife'),
)

class session_attended_options(models.Model):
    session_attended = models.CharField(max_length=30, choices=session_attended, null=False, blank=False)
    group_leader =  models.ForeignKey(User, models.CASCADE, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.session_attended}'



class session_attendance(models.Model):
    attendee = models.ForeignKey(People, models.CASCADE, null=True)
    dateofvisit = models.DateField(default=datetime.date.today(), verbose_name = 'Date:')
    session_attended = models.ForeignKey(session_attended_options, models.CASCADE, null=False, blank=False)
    createdby =  models.ForeignKey(User, models.CASCADE, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.createdby}, {self.attendee}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['attendee', 'dateofvisit', 'session_attended'], name="%(app_label)s_%(class)s_unique")
        ]

class group_membership(models.Model):
    member = models.ForeignKey(People, models.CASCADE, null=True)
    group = models.ForeignKey(session_attended_options, models.CASCADE, null=True)
    active = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return f'{self.member}, {self.group}, {self.active}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['member', 'group'], name="%(app_label)s_%(class)s_unique")
        ]

class prayer_cell_feedback(models.Model):
    date_of_meeting = models.DateField(verbose_name= 'Date of meeting:')
    disciple_leader = models.ForeignKey(People, models.CASCADE, null=False)
    word_discussed = models.TextField(verbose_name= 'Word Discussed:')
    prayed_about = models.TextField(verbose_name='Prayed About:')
    testimonies = models.TextField(verbose_name='Testimonies:', null=True, blank=True)
    prayer_requests = models.TextField(verbose_name='Prayer Requests', null=True, blank=True)
    meeting_hosted = models.ForeignKey(session_attended_options, models.CASCADE, null=False)
