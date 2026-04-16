from django.db import models
from django.conf import settings

class Task(models.Model):
    PRIORITY_CHOICES = [('low', 'Past'), ('medium', 'Oʻrta'), ('high', 'Yuqori')]
    STATUS_CHOICES = [('todo', 'Bajarilishi kerak'), ('doing', 'Jarayonda'), ('done', 'Bajarildi')]

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title