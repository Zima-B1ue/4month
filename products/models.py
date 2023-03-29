from django.db import models


# Create your models here.

class Product(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.FloatField(0.0)
    created_date = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)


class Comment(models.Model):
    text = models.CharField(max_length=255)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
