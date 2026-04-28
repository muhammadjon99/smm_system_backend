from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import User

phone_validator = RegexValidator(
    regex=r'^\+998(33|50|77|88|90|91|93|94|95|97|98|99)\d{7}$',
    message="Telefon raqami noto'g'ri formatda yoki operator kodi xato (masalan: +998901234567)."
)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    phone = serializers.CharField(validators=[phone_validator])
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'phone', 'role']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
