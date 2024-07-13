from .models import Converts, Followups, Followed_Up_by
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(pre_save, sender=Followups)
def create_followed_up_by(sender, instance, **kwargs):
    if not instance._state.adding:
            Followed_Up_by.objects.create(convert=instance)
            
    else:
            print ('this is an insert')