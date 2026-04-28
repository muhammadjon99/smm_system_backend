from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .models import Task
from .serializers import TaskSerializer

@extend_schema(tags=['Tasks'])
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related('order', 'order__client').order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'assigned_to']
    def get_queryset(self):
        user = self.request.user
        base_queryset = Task.objects.all().select_related('order', 'order__client').order_by('-created_at')
        if user.is_staff or getattr(user, 'role', None) == 'manager':
            return base_queryset

        return base_queryset.filter(assigned_to=user)