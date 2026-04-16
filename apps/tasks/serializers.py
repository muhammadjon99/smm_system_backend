from rest_framework import serializers
from .models import Task
from apps.accounts.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to',
            'assigned_to_detail', 'status', 'priority',
            'deadline', 'created_at'
        ]