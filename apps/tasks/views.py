from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'assigned_to']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager' or user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)