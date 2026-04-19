from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().select_related('client')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['client', 'is_confirmed', 'method']