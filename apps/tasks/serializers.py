from rest_framework import serializers
from django.utils import timezone
from .models import Task
from apps.accounts.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    is_overdue = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = [
            'id', 'order', 'title', 'description', 'assigned_to',
            'assigned_to_detail', 'status', 'priority',
            'deadline', 'is_overdue', 'created_at'
        ]
    def get_is_overdue(self, obj):
        if obj.deadline and obj.status != 'completed':
            return obj.deadline < timezone.now()
        return False