from django.db import models


# Create your models here.

class Products(models.Model):
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    rate = models.FloatField()
