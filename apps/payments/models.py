from django.db import models
from django.core.exceptions import ValidationError

class Payment(models.Model):
    class Method(models.TextChoices):
        CLICK = 'click', 'Click'
        PAYME = 'payme', 'Payme'
        CASH = 'cash', 'Naqd'
        TRANSFER = 'transfer', 'O\'tkazma'

    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="To'lov summasi")
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.CASH)
    is_confirmed = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Tasdiqlangan" if self.is_confirmed else "Kutilmoqda"
        return f"{self.client.name} - {self.amount} ({status})"