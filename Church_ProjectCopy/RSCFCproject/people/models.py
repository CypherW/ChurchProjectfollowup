from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

# Create your models here.
class People(models.Model):
    Name = models.CharField(max_length=20, null=False, blank=False)
    Surname = models.CharField(max_length=20, null=False, blank=False)
    Gender = models.CharField(max_length=7, choices=GENDER, null=True, blank=False)
    CellNumber = models.CharField(max_length=10, null=True, blank=True)
    EmailAddress = models.EmailField(max_length=50, null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    area = models.CharField(max_length=20, null=False, blank=False)
    createdBy = models.ForeignKey(User, models.CASCADE, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name_plural = 'People'

    class Meta:
        ordering = ['-date']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Name', 'Surname'], name="%(app_label)s_%(class)s_unique")
        ]


    def __str__(self):
        return f'{self.Name} {self.Surname}'

    @property
    def age(self):
        if self.birthday == None:
            age = "TBC"
        else:
            today = timezone.now().date()
            age = int(
            today.year
                - (self.birthday.year)
                - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        )
        return age

class guardianRelation(models.Model):
    child = models.ForeignKey(People, on_delete=models.CASCADE, related_name='guardians_as_child')
    parent = models.ForeignKey(People, on_delete=models.CASCADE, related_name='guardians_as_parent')

    class Meta:
        verbose_name_plural = 'Guardian'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child', 'parent'], name="%(app_label)s_%(class)s_unique")
        ]