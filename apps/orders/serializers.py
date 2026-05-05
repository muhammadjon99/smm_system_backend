from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'client', 'service', 'quantity', 'total_price', 'status', 'status_display', 'created_at']

    def validate(self, data):
        if data.get('quantity') and data['quantity'] <= 0:
            raise serializers.ValidationError({"quantity": "Miqdor 0 dan katta bo'lishi shart."})
        return data

    def create(self, validated_data):
        return super().create(validated_data)