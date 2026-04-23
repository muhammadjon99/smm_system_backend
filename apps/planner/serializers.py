from rest_framework import serializers
from .models import Client


class ClientDashboardSerializer(serializers.ModelSerializer):
    active_orders_count = serializers.SerializerMethodField()
    monthly_spending = serializers.SerializerMethodField()
    content_stats = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = '__all__'
    def get_active_orders_count(self, obj):
        return obj.orders.filter(status='processing').count()
    def get_monthly_spending(self, obj):
        return sum(order.total_price for order in obj.orders.all())

    def get_content_stats(self, obj):
        return {
            'pending': obj.plans.filter(status='pending').count(),
            'approved': obj.plans.filter(status='approved').count(),
            'published': obj.plans.filter(status='published').count(),
        }