from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
