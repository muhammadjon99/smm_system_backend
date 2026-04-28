from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import Payment

@receiver(post_save, sender=Payment)
def update_client_stats(sender, instance, **kwargs):
    client = instance.client
    total = Payment.objects.filter(
        client=client,
        is_confirmed=True
    ).aggregate(total=Sum('amount'))['total'] or 0
    client.total_paid = total
    client.save(update_fields=['total_paid'])