from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('client', 'service')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'created_at']
    search_fields = ['client__phone', 'client__name']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class DashboardAnalyticsView(APIView):
    def get(self, request):
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        orders_by_status = Order.objects.values('status').annotate(count=Count('id'))

        return Response({
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'orders_by_status': orders_by_status
        })
