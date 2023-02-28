from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Ingredient(models.Model):
    
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=7)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ingredients", null=True)

    def __str__(self):
        return f"{self.name}"

class Recipe (models.Model):
    title = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images', blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes", blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes", null=True)
    type = models.CharField(max_length=20)
    serv = models.IntegerField()
    inst = models.TextField()

    def __str__(self):
        return self.title
