from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from apps.tasks.models import Task
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender=Order)
def create_automated_tasks(sender, instance, created, **kwargs):
    if created:
        Task.objects.create(
            order=instance,
            title=f"Yangi buyurtma uchun kontent-plan: {instance.client.name}",
            description=f"Tarif: {instance.service.name}. {instance.service.post_limit} ta post tayyorlash kerak.",
            deadline=timezone.now() + timedelta(days=2),
            priority='high'
        )