from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("To'lov summasi 0 dan katta bo'lishi shart.")
        return data