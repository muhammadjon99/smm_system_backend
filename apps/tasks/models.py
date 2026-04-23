from django.db import models
from django.conf import settings

class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'low', 'Past'
        MEDIUM = 'medium', 'O\'rta'
        HIGH = 'high', 'Yuqori'
    class Status(models.TextChoices):
        TODO = 'todo', 'Bajarilishi kerak'
        IN_PROGRESS = 'in_progress', 'Jarayonda'
        DONE = 'done', 'Bajarildi'
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title