from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    stock = models.IntegerField()
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="product_category",
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(
        upload_to="foods", default="foods/default.jpg", blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ProductGroup(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(
        "products.Product", related_name="productgroups", blank=True
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def total_price(self):
        return sum(products.price for products in self.products.all())

    def __str__(self):
        return self.name
