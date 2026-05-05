from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "To'lov summasi 0 dan katta bo'lishi shart. Iltimos, musbat son kiriting.")
        return value

    def validate(self, data):
        instance = Payment(**data)
        try:
            instance.clean()
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return data