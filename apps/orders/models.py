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
        if self.service.price is None or self.service.price <= 0:
            raise ValidationError({
                'service': f"'{self.service.name}' xizmati narxi noto'g'ri ko'rsatilgan. Iltimos, administratorga murojaat qiling."
            })
        if self.quantity < 1:
            raise ValidationError({'quantity': "Miqdor kamida 1 bo'lishi kerak."})
        if not self.pk:
            check_order_limits(self.client, self.service)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.total_price = Decimal(self.service.price) * Decimal(self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.client.name}"