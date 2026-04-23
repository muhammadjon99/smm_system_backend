from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='client_logos/', blank=True, null=True)
    insta_username = models.CharField(max_length=100, blank=True, null=True)
    insta_password = models.CharField(max_length=255, blank=True, null=True)
    initial_followers = models.PositiveIntegerField(default=0)
    current_followers = models.PositiveIntegerField(default=0)
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name