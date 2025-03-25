from django.db import models
from django.conf import settings


class Recipe(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_group = models.ForeignKey(
        "products.ProductGroup",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="recipes",
    )

    def __str__(self):
        return self.name
