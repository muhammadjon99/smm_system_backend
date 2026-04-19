from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    video_limit = models.PositiveIntegerField(default=0)
    post_limit = models.PositiveIntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.name