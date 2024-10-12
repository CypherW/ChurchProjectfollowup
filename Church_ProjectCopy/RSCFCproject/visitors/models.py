from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from SalvationFollowUps.models import Converts
from people.models import People
from groups.models import session_attended_options

# Create your models here.

ContactPreference = (
    ('Phone', 'Phone'),
    ('Email', 'Email'),
)

first_contact_method = (
    ('Whatsapp', 'Whatsapp'),
    ('Email', 'Email'),
)

add_to_whatsapp_group = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

class visit_details(models.Model):
    visitor = models.ForeignKey(People, models.CASCADE, null=True)
    dateofvisit = models.DateField(default=timezone.now, verbose_name = 'Date:')
    contactMethod = models.CharField(max_length=20, choices=ContactPreference, null=False, blank=False, default='Unspecified')
    
    class Meta:
        verbose_name_plural = 'visitor'

    def __str__(self):
        return f'{self.visitor} {self.dateofvisit} {self.contactMethod}'
    
class visitor_first_followup(models.Model):
    visitor = models.ForeignKey(visit_details, models.CASCADE, null=False)
    method_of_followup = models.CharField(max_length=20, choices=first_contact_method, null=False, blank=False, default='Unspecified')
    response = models.TextField(verbose_name='Response:', null=True, blank=True)
    added_to_Whatsapp_group = models.CharField(max_length=5, choices=add_to_whatsapp_group, null=False, blank=False, default="Unspecified")
    followedup_up_by = models.ForeignKey(User, models.CASCADE, null=False)
    date_of_followup = models.DateField(default=timezone.now, verbose_name = 'Date:')

    class Meta:
        verbose_name_plural = 'Visitor First Follow up'

    def __str__(self):
        return f'{self.visitor} {self.method_of_followup} {self.response} {self.added_to_Whatsapp_group} {self.followedup_up_by} {self.date_of_followup}'

class visitor_followup_call(models.Model):
    visitor = models.ForeignKey(visit_details, models.CASCADE, null=False)
    general_feedback = models.TextField(verbose_name='Feedback:', null=False, blank=False)
    prayer_request = models.TextField(verbose_name='Prayer Request', null=True, blank=True)
    date_of_followup = models.DateField(default=timezone.now, verbose_name = 'Date:')
    followedup_up_by = models.ForeignKey(User, models.CASCADE, null=False)

    class Meta:
        verbose_name_plural = 'Visitor Follow up call'

    def __str__(self):
        return f'{self.visitor} {self.general_feedback} {self.prayer_request} {self.date_of_followup} {self.followedup_up_by}'
    
class visitor_referral_finalize(models.Model):
    visitor = models.ForeignKey(visit_details, models.CASCADE, null=False)
    refer_to_church = models.TextField(verbose_name='Refer to another church:', null=True, blank=True)
    refer_to_prayer_cell = models.ForeignKey(session_attended_options, models.CASCADE, null=True, blank=True)
    finalize = models.BooleanField(null=False, blank=False)
    date_of_followup = models.DateField(default=timezone.now, verbose_name = 'Date:')
    followedup_up_by = models.ForeignKey(User, models.CASCADE, null=False)

    class Meta:
        verbose_name_plural = 'Visitor Referral and Finalize'

    def __str__(self):
        return f'{self.visitor} {self.refer_to_church} {self.refer_to_prayer_cell} {self.finalize} {self.date_of_followup} {self.followedup_up_by}'


#### OLD TO BE DELETED ####

class visit_date(models.Model):
    visitor = models.OneToOneField(Converts, models.CASCADE, null=True)
    createdby =  models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    dateofvisit = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'{self.createdby}, {self.convert}'