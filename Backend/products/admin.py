from django.contrib import admin
from .models import Product, ProductGroup, ProductGroupItem


class ProductGroupItemInline(admin.TabularInline):
    model = ProductGroupItem
    fields = ("product",)
    readonly_fields = ()

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("name", "stock", "category", "description", "price")
    prepopulated_fields = {"slug": ["name"]}


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ("name", )
    inlines = [ProductGroupItemInline]


@admin.register(ProductGroupItem)
class ProductGroupItemAdmin(admin.ModelAdmin):
    list_display = ("product",)
    filter_horizontal = ()