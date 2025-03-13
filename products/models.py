from django.db import models
from PIL import Image
from django.core.files import File
from io import BytesIO
class Product(models.Model):
    class Category(models.TextChoices):
        FRUITS = 'FR', 'Fruits'
        VEGETABLES = 'VE', 'Vegetables'
        MEATS = 'MT', 'Meats'
        DAIRY = 'DA', 'Dairy'
        HYGIENE = 'HY', 'Hygiene'
        CLEANING = 'CL', 'Cleaning'
        FROZEN = 'FZ', 'Frozen'
        SEA_FOOD = 'SF', 'Sea Food'
        PRESERVES = 'PR', 'Preserves'
        BAKED_GOODS = 'BG', 'Baked Goods'
    name= models.CharField(max_length=100)
    stock= models.IntegerField()
    category=models.CharField(max_length=2, choices=Category.choices)
    description=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    image=models.ImageField(upload_to='Food',blank=True,null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

    
class ProductGroup(models.Model):
    name=models.CharField(max_length=100)
    products=models.ForeignKey('products.Product',related_name='productgroups',on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=6,decimal_places=2)

    @property
    def price(self):
        return sum(products.price for products in self.products.all())