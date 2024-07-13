from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from SalvationFollowUps.models import Converts

# Create your models here.

class visit_date(models.Model):
    visitor = models.OneToOneField(Converts, models.CASCADE, null=True)
    createdby =  models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    dateofvisit = models.DateTimeField(default=datetime.date.today())


    def __str__(self):
        return f'{self.createdby}, {self.convert}'