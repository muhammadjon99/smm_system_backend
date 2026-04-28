from django.db import models
from apps.clients.models import Client
from simple_history.models import HistoricalRecords

class ContentPlan(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('pending', 'Tasdiq kutilmoqda'),
        ('approved', 'Tasdiqlandi'),
        ('rejected', 'Inkor qilindi'),
        ('published', 'Post qilindi'),
    ]
    history = HistoricalRecords()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Post ssenariysi yoki matni")
    image = models.ImageField(upload_to='planner/images/', blank=True, null=True)
    post_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    feedback = models.TextField(blank=True, null=True, help_text="Mijozning e'tirozlari (Reject bo'lsa)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} - {self.post_date} - {self.title}"