# filepath: /home/mohamed/galawave/user_auth/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser, UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # If user is superuser, create profile with admin role
        if instance.is_superuser:
            UserProfile.objects.create(
                user=instance,
                role='admin',
            )
