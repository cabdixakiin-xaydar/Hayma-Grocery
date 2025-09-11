from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_blocked = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.username

# Create your models here.
