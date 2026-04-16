from django.db import models
from apps.clients.models import Client
from apps.services.models import Service

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Jarayonda'),
        ('done', 'Bajarildi'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.service.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.name} - {self.service.name}"