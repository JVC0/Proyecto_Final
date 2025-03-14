from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Token

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'key',
        'created_at',
    )