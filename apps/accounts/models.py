from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+998(33|50|70|77|88|90|91|93|94|95|97|98|99)\d{7}$',
    message="Telefon raqami noto'g'ri formatda yoki operator kodi xato (masalan: +998901234567)."
)

class User(AbstractUser):
    phone = models.CharField(
        max_length=13,
        validators=[phone_validator],
        unique=True,
        null=True,
        blank=True,
        help_text="Format: +998901234567"
    )
    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('client', 'Client'),
        ],
        default='admin'
    )
    def __str__(self):
        return f"{self.username} - {self.role} ({self.phone if self.phone else 'No phone'})"