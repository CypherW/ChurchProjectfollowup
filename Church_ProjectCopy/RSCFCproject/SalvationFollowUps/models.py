from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from people.models import People

# Create your models here.

ContactPreference = (
    ('Phone', 'Phone'),
    ('Email', 'Email'),
)

decission = (
    ('First Time', 'First Time'),
    ('Rededication', 'Rededication'),
)

preferred_language = (
    ('African', 'African'),
    ('Afrikaans', 'Afrikaans'),
    ('English', 'English'),

)

attending_church = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

first_contact_method = (
    ('Whatsapp', 'Whatsapp'),
    ('Email', 'Email'),
)

add_to_whatsapp_group = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)


class salvations(models.Model):
    convert = models.ForeignKey(People, models.CASCADE, null=True)
    dateofcommitment = models.DateField(default=timezone.now, verbose_name = 'Date:')
    contactMethod = models.CharField(max_length=20, choices=ContactPreference, null=False, blank=False, default='Unspecified')
    decissionType = models.CharField(max_length=20, choices=decission, null=False, blank=False, default="Unspecified")

    class Meta:
        verbose_name_plural = 'Salvations'

    def __str__(self):
        return f'{self.convert} {self.dateofcommitment} {self.contactMethod} {self.decissionType}'
    
class new_convert_first_followup(models.Model):
    convert = models.ForeignKey(salvations, models.CASCADE, null=False)
    method_of_followup = models.CharField(max_length=20, choices=first_contact_method, null=False, blank=False, default='Unspecified')
    response = models.TextField(verbose_name='Response:', null=True, blank=True)
    added_to_Whatsapp_group = models.CharField(max_length=5, choices=add_to_whatsapp_group, null=False, blank=False, default="Unspecified")
    followedup_up_by = models.ForeignKey(User, models.CASCADE, null=False)
    date_of_followup = models.DateField(default=timezone.now, verbose_name = 'Date:')

    class Meta:
        verbose_name_plural = 'New Convert First Follow up'

    def __str__(self):
        return f'{self.convert} {self.method_of_followup} {self.response} {self.added_to_Whatsapp_group} {self.followedup_up_by} {self.date_of_followup}'

class new_convert_followup_call(models.Model):
    convert = models.ForeignKey(salvations, models.CASCADE, null=False)
    general_feedback = models.TextField(verbose_name='Feedback:', null=False, blank=False)
    prayer_request = models.TextField(verbose_name='Prayer Request', null=True, blank=True)
    date_of_followup = models.DateField(default=timezone.now, verbose_name = 'Date:')
    followedup_up_by = models.ForeignKey(User, models.CASCADE, null=False)

    class Meta:
        verbose_name_plural = 'New Convert Follow up'

    def __str__(self):
        return f'{self.convert} {self.general_feedback} {self.prayer_request} {self.date_of_followup} {self.followedup_up_by}'


##### OLD MODELS - NEED TO BE REMOVED
LANGUAGE = (
    ('African', 'African'),
    ('Afrikaans', 'Afrikaans'),
    ('English', 'English'),    
)

ATTENDCHURCH = (
    ('Unkown', 'Unkown'),
    ('RSCFC', 'RSCFC'),
    ('Local No', 'Local No'),
    ('Another Church', 'Another Church'),
    ('Away: want to be connected', 'Away: want to be connected'),
    ('Connected', 'Connected'),

)

CONVERSIONVENUE = (
    ('FaithKids', 'FaithKids'),
    ('Online', 'Online'),
    ('Outreach', 'Outreach'),
    ('RSCFC Auditorium', 'RSCFC Auditorium'),
    ('Ylife', 'Ylife'),
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

LINK_CHURCHES = (
    ('Rhema Randburg', 'Rhema Randburg'),
    ('Rhema South', 'Rhema South'),

)


class Converts(models.Model):
    createdBy = models.ForeignKey(User, models.CASCADE, null=True)
    Name = models.CharField(max_length=20, null=False, blank=False)
    Surname = models.CharField(max_length=20, null=False, blank=False)
    Gender = models.CharField(max_length=7, choices=GENDER, null=False, blank=True)
    CellNumber = models.CharField(max_length=10, null=False, blank=True)
    EmailAddress = models.EmailField(max_length=50, null=False, blank=True)
    whereConverted = models.CharField(max_length=20, choices=CONVERSIONVENUE, null=False, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    area = models.CharField(max_length=20, null=False, blank=True)
    

    class Meta:
        verbose_name_plural = 'Convert'

    class Meta:
        ordering = ['-date']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Name', 'Surname'], name="%(app_label)s_%(class)s_unique")
        ]


    def __str__(self):
        return f'{self.Name} {self.Surname}'

    def conversionVenues(self):
        newlist = []
        for item in self:
            newlist.append(item.whereConverted)
        return list(set(newlist))

    def catConversionTotal(self, venues):
        totals = []
        for venue in venues:
            num = 0
            for conversion in self:
                if conversion.whereConverted == venue:
                    num += 1
            totals.append(num)
        return totals

class Followups(models.Model):
    createdBy = models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    convert = models.OneToOneField(Converts, on_delete=models.CASCADE, primary_key=True)
    Language = models.CharField(max_length=20, choices=LANGUAGE, null=False, blank=True)
    AttendChurch = models.CharField(max_length=30, choices=ATTENDCHURCH, null=False, blank=False, default='Unknown')
    date = models.DateTimeField(auto_now_add=True)
    next_followUpdate = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Followups'

    class Meta:
        ordering = ["next_followUpdate"]
    

    def __str__(self):
        return f'{self.convert} created by due {self.next_followUpdate}'

    def AttendChurchCat(self):
        attendList = []
        for status in self:
            attendList.append(status.AttendChurch)
        return list(set(attendList)) 

    def churchAttendCatTotals(self, attendCats):
        catTotal = []
        for category in attendCats:
            num = 0
            for attendStatus in self:
                if category == attendStatus.AttendChurch:
                    num += 1
            catTotal.append(num)
        return catTotal

class Followed_Up_by(models.Model):
    convert = models.ForeignKey(Followups, models.CASCADE, null=True)
    createdby =  models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.createdby}, {self.convert}'

class Requests_Feedback(models.Model):
    createdBy = models.ForeignKey(User, models.CASCADE, null=True)
    convert = models.OneToOneField(Converts, on_delete=models.CASCADE, primary_key=True)
    PrayerRequest = models.CharField(max_length=200, null=False, blank=True)
    General = models.CharField(max_length=200, null=False, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Prayer Requests & Feedback'

    def __str__(self):
        return f'{self.convert} created by {self.createdBy.username}'

        
class Link_Church(models.Model):
    createdBy = models.ForeignKey(User, models.CASCADE, null=True)
    convert = models.OneToOneField(Followups, on_delete=models.CASCADE, primary_key=True)
    church_name = models.CharField(max_length=40,choices=LINK_CHURCHES, null=False, blank=False)
    church_area = models.CharField(max_length=20, null=False, blank=True)
    church_phone_number = models.CharField(max_length=10, null=False, blank=True)
    church_contact_name = models.CharField(max_length=30, null=False, blank=True)

    def __str__(self):
        return f'{self.convert} {self.church_name}'
