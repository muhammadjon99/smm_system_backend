from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    # Total price faqat o'qish uchun, uni save() metodimiz hisoblaydi
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'