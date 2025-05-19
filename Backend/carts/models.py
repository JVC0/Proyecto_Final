from django.db import models

# Create your models here.


class Cart(models.Model):
    profile = models.ForeignKey(
        "users.Profile", related_name="cart", on_delete=models.CASCADE
    )
    products = models.ManyToManyField(
        "products.Product", through="CartItem", related_name="carts"
    )

    @property
    def total_price(self):
        return sum(
            item.product.price * item.quantity
            for item in self.cartitems.all()
            if item.product.price is not None
        )

    def __str__(self):
        return f"Cart for {self.profile}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product} in {self.cart}"
