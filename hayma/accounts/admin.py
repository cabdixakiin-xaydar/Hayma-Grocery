from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Additional info', {'fields': ('phone', 'address', 'is_blocked')}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_blocked')

# Register your models here.
