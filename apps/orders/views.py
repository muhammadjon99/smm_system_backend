from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count
from rest_framework import viewsets, permissions



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['status', 'client', 'service']
    search_fields = ['client__name', 'service__name']

    def perform_create(self, serializer):
        serializer.save()

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