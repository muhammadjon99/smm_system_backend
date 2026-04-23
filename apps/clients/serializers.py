from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    active_orders_count = serializers.SerializerMethodField()
    content_stats = serializers.SerializerMethodField()
    followers_growth = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'phone', 'address', 'logo', 'insta_username', 'initial_followers', 'current_followers',
            'monthly_budget', 'created_at', 'active_orders_count', 'content_stats', 'followers_growth'
        ]

    def get_active_orders_count(self, obj):
        return obj.orders.count()

    def get_followers_growth(self, obj):
        return obj.current_followers - obj.initial_followers

    def get_content_stats(self, obj):
        return {
            'pending': obj.plans.filter(status='pending').count(),
            'approved': obj.plans.filter(status='approved').count(),
            'published': obj.plans.filter(status='published').count(),
        }
