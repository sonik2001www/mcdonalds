from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    calories = models.CharField(max_length=255)
    fats = models.CharField(max_length=255)
    carbs = models.CharField(max_length=255)
    proteins = models.CharField(max_length=255)
    unsaturated_fats = models.CharField(max_length=255)
    sugar = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    portion = models.CharField(max_length=255)
