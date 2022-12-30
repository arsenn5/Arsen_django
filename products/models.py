from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)


class Products(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    rate = models.FloatField()
    category = models.ManyToManyField(Category)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, related_name='review')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
