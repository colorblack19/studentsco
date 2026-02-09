from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserStatus
from django.contrib.auth.signals import user_logged_out

@receiver(post_save, sender=User)
def create_user_status(sender, instance, created, **kwargs):
    if created:
        UserStatus.objects.create(user=instance)



@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    try:
        status = UserStatus.objects.get(user=user)
        status.is_online = False
        status.save(update_fields=["is_online"])
    except UserStatus.DoesNotExist:
        pass
