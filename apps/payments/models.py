from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

class Payment(models.Model):
    class Method(models.TextChoices):
        CLICK = 'click', 'Click'
        PAYME = 'payme', 'Payme'
        CASH = 'cash', 'Naqd'
        TRANSFER = 'transfer', 'O\'tkazma'
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments', null=True)
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="To'lov summasi")
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.CASH)
    is_confirmed = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if not self.order:
            raise ValidationError("To'lov qaysi buyurtma uchun qilinayotganini ko'rsatish shart.")
        total_order_price = self.order.total_price
        already_paid = Payment.objects.filter(
            order=self.order,
            is_confirmed=True
        ).exclude(pk=self.pk).aggregate(Sum('amount'))['amount__sum'] or 0
        remaining_debt = total_order_price - already_paid
        if self.amount > remaining_debt:
            raise ValidationError(
                f"Ortiqcha to'lov! Buyurtma bo'yicha qolgan qarz: {remaining_debt} so'm. "
                f"Siz esa {self.amount} so'm kiritdingiz."
            )
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        status = "Tasdiqlangan" if self.is_confirmed else "Kutilmoqda"
        order_info = f" (Order: {self.order.order_number})" if self.order else ""
        return f"{self.client.name} - {self.amount}{order_info} ({status})"