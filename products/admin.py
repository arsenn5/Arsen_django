from django.contrib import admin
from products.models import Products, Review, Category


admin.site.register(Products)
admin.site.register(Review)
admin.site.register(Category)