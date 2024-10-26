from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from people.models import People

# Create your models here.
service_attended = (
    ('1', '1st Service'),
    ('2', '2nd Service'),
)

class service_counts(models.Model):
    service_date = models.DateField(default=timezone.now, verbose_name = 'Date:')
    first_service_count = models.IntegerField(null=True, blank=True, default=0)
    second_service_count = models.IntegerField(null=True, blank=True, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    counter = models.ForeignKey(User, models.CASCADE, null=False)

    def __str__(self):
        return f'{self.service_date}, {self.first_service_count}, {self.second_service_count}, {self.creation_date}, {self.counter}'
    
class childrensChurch_classes(models.Model):
    class_name = models.CharField(max_length=30, null=False, blank=False)
    head_teacher = models.ForeignKey(User, models.CASCADE, null=False)

    def __str__(self):
        return f'{self.class_name}, {self.head_teacher}'


class childrensChurch_teachers(models.Model):
    teacher = models.ForeignKey(User, models.CASCADE, null=False)
    classes = models.ManyToManyField(childrensChurch_classes)

    def __str__(self):
        return f'{self.teacher}, {self.classes}'

class childrensChurch_class_member(models.Model):
    child = models.ForeignKey(People, models.CASCADE, null=False)
    class_attending = models.ForeignKey(childrensChurch_classes, models.CASCADE, null=False)
    active = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return f'{self.child}, {self.class_attending}, {self.active}'
    
class class_attendance(models.Model):
    child = models.ForeignKey(childrensChurch_class_member, models.CASCADE, null=False)
    class_name = models.ForeignKey(childrensChurch_classes, models.CASCADE, null=False)
    dateofclass =  models.DateField(default=timezone.now, verbose_name = 'Date:')
    service = models.CharField(max_length=3, choices=service_attended)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.CASCADE, null=False)

    def __str__(self):
        return f'{self.child}, {self.class_name}, {self.dateofclass}, {self.service}, {self.creation_date}, {self.created_by}'

class class_service_feedback(models.Model):
    teachers = models.ManyToManyField(childrensChurch_teachers)
    class_name = models.ForeignKey(childrensChurch_classes, models.CASCADE, null=False)
    word_taught = models.TextField(verbose_name= 'Word Taught:')
    general_feedback = models.TextField(verbose_name= 'General Feedback:')
    requires_attention = models.TextField(verbose_name= 'Requires Attention:')
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.CASCADE, null=False)
    
    def __str__(self):
        return f'{self.teachers}, {self.class_name}, {self.word_taught}, {self.general_feedback}, {self.requires_attention}, {self.creation_date}, {self.created_by}'