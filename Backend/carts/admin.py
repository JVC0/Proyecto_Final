from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ("product", "quantity")
    readonly_fields = ("product",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user_email", "total_items", "total_price")
    inlines = [CartItemInline]

    def user_email(self, obj):
        return obj.profile.user.email

    user_email.short_description = "User"

    def total_items(self, obj):
        return obj.cartitems.count()

    total_items.short_description = "Items"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")
    list_filter = ("cart", "product")
