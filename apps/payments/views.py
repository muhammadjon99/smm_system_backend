from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Payments'])
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().select_related('client', 'order')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['method', 'is_confirmed']

    def get_queryset(self):
        user = self.request.user
        base_queryset = Payment.objects.select_related('client', 'order').order_by('-created_at')
        if user.is_staff or getattr(user, 'role', None) == 'manager':
            return base_queryset
        return base_queryset.filter(client__user=user)
    def perform_create(self, serializer):
        serializer.save(is_confirmed=False)