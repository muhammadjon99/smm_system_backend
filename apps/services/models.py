from django.db import models

class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('video', 'Video'),
        ('post', 'Post'),
        ('story', 'Story'),
        ('reels', 'Reels'),
    ]
    name = models.CharField(max_length=100)
    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        default='post'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"