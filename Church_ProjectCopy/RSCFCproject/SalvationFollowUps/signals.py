from .models import Converts, Followups
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=Converts)
def create_followup_convert(sender, instance, created, **kwargs):
    if created:
        Followups.objects.create(convert=instance)