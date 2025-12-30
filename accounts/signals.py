from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import TeacherProfile

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        if instance.groups.filter(name="Teacher - Basic").exists():
            TeacherProfile.objects.get_or_create(user=instance)
