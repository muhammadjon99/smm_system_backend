from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.tasks.models import Task
from .models import Client
from .serializers import ClientSerializer
from rest_framework.permissions import AllowAny
from django.db.models import Sum,Count
from apps.payments.models import Payment
from apps.orders.models import Order
from django.utils import timezone
from rest_framework.views import APIView

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    @action(detail=True, methods=['get'], permission_classes = [AllowAny])
    def statistics(self, request, pk=None):
        client = self.get_object()
        total_spent = sum(o.total_price for o in client.orders.all()) or 0
        initial = client.initial_followers or 0
        current = client.current_followers or 0
        growth = current - initial
        data = {
            'client_name': client.name,
            'total_orders': client.orders.count(),
            'total_spent': total_spent,
            'active_tasks': Task.objects.filter(order__client=client, status='todo').count(),
            'followers_growth': growth,
            'content_stats': {
                'pending': client.plans.filter(status='pending').count(),
                'approved': client.plans.filter(status='approved').count(),
                'published': client.plans.filter(status='published').count(),
            }
        }
        return Response(data)


class AdminDashboardAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        today = timezone.now().date()
        daily_revenue = Payment.objects.filter(
            created_at__date=today,
            is_confirmed=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        total_clients = Client.objects.count()
        total_orders = Order.objects.count()
        total_revenue = Payment.objects.filter(
            is_confirmed=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        top_service_query = Order.objects.values('service_name').annotate(
            count=Count('id')
        ).order_by('-count').first()
        top_service = top_service_query['service_name'] if top_service_query else "Noma'lum"
        return Response({
            'daily_stats': {
                'revenue': daily_revenue,
                'orders_today': Order.objects.filter(created_at__date=today).count(),
            },
            'overall_stats': {
                'total_clients': total_clients,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
            },
            'popular': {
                'top_service': top_service
            }
        })