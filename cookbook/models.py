from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Ingredient(models.Model):
    ING_CATEGORIES = (
        ('V', 'Vegetables'),
        ('SH', 'Spices and Herbs'),
        ('CP', 'Cereals and Pulses'),
        ('M', 'Meat'),
        ('D', 'Dairy Products'),
        ('F', 'Fruits'),
        ('S', 'Seafood'),
        ('SP', 'Sugar and Sugar Produts<')
    )

    name = models.CharField(max_length=64)
    category = models.CharField(max_length=2, choices=ING_CATEGORIES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ingredients", null=True)

    def __str__(self):
        return f"{self.name}"