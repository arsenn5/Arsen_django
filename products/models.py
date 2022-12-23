from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)

class Products(models.Model):
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    rate = models.FloatField()
    category = models.ManyToManyField(Category)

class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, related_name='review')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
