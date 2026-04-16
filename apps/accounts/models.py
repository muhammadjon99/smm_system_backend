from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('client', 'Client'),
    ], default='admin')

    def __str__(self):
        return f"{self.username} - {self.role}"