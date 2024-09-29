from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class service_counts(models.Model):
    service_date = models.DateField(default=timezone.now, verbose_name = 'Date:')
    first_service_count = models.IntegerField(null=True, blank=True, default=0)
    second_service_count = models.IntegerField(null=True, blank=True, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    counter = models.ForeignKey(User, models.CASCADE, null=False)

    def __str__(self):
        return f'{self.service_date}, {self.first_service_count}, {self.second_service_count}, {self.creation_date}, {self.counter}'

