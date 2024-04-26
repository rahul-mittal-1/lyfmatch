from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, CustomUser
import uuid

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile_id = str(uuid.uuid4())[:10]  # Generate a unique profile ID
        Profile.objects.create(user=instance, profile_id=profile_id)