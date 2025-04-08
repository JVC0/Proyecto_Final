from django.contrib import admin
from .models import Product, ProductGroup


from django.contrib import admin
from .models import Product, ProductGroup


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("name", "stock", "category", "description", "price")
    prepopulated_fields = {"slug": ["name"]}


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ("name", )
    filter_horizontal = ("products",)
