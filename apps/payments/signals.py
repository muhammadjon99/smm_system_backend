from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment

@receiver(post_save, sender=Payment)
def update_client_stats(sender, instance, created, **kwargs):
    if instance.is_confirmed:
        client = instance.client
        client.monthly_budget = sum(p.amount for p in client.payments.filter(is_confirmed=True))
        client.save()