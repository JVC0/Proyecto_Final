from django.contrib import admin
from .models import Product
@admin.register(Product)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'stock',
        'category',
        'description',
        'price'
    )
    
