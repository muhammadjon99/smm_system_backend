from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from .services import check_order_limits

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Kutilmoqda'
        PROCESSING = 'processing', 'Jarayonda'
        COMPLETED = 'completed', 'Bajarildi'
        CANCELLED = 'cancelled', 'Bekor qilindi'
        FAILED = 'failed', 'Xatolik yuz berdi'
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey('services.Service', on_delete=models.PROTECT, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if not self.service:
            raise ValidationError({'service': "Xizmat tanlanishi shart."})
        if not self.pk:
            check_order_limits(self.client, self.service)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.price_at_order = self.service.price
        self.total_price = Decimal(self.price_at_order) * Decimal(self.quantity)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Order #{self.id} - {self.client.name}"