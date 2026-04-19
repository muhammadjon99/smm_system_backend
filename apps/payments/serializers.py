from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    client_name = serializers.ReadOnlyField(source='client.name')

    class Meta:
        model = Payment
        fields = [
            'id', 'client', 'client_name', 'amount',
            'method', 'is_confirmed', 'transaction_id', 'created_at'
        ]