from django.db import models

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
    




    def __str__(self):
        return self.name