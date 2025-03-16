from django.conf import settings
from django.db import models
import uuid


class Profile(models.Model):

    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to="avatars",
        default="avatars/noavatar.jpg",
    )
    bio = models.TextField(blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.ForeignKey(
        "users.Token", related_name="profiles", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Token(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="token"
    )
    key = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"
