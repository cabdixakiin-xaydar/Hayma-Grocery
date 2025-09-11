from django.contrib import admin
from .models import Category, Product, Coupon

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Coupon)

# Register your models here.
