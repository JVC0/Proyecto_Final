from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Token, Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_token_and_profile(sender, instance, created, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        Profile.objects.create(user=instance, token=token)
