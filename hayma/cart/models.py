from django.db import models
from django.conf import settings
from catalog.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Cart of {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self) -> str:
        return f"{self.product} x {self.quantity}"

# Create your models here.
