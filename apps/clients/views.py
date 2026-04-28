from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.tasks.models import Task
from .models import Client
from .serializers import ClientSerializer
from django.db.models import Sum, Count, Q
from apps.payments.models import Payment
from apps.orders.models import Order
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().select_related('user').order_by('-created_at')
    serializer_class = ClientSerializer

    @extend_schema(tags=['Clients'])
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        client = Client.objects.filter(pk=pk).annotate(
            total_orders=Count('orders', distinct=True),
            total_spent=Sum('orders__total_price'),
            active_tasks=Count('orders__tasks', filter=Q(orders__tasks__status='todo'), distinct=True),
            pending_plans=Count('plans', filter=Q(plans__status='pending'), distinct=True),
            approved_plans=Count('plans', filter=Q(plans__status='approved'), distinct=True),
            published_plans=Count('plans',
                                  filter=Q(plans__status='published').distinct() if hasattr(self, 'distinct') else Q(
                                      plans__status='published'), distinct=True),
        ).first()

        if not client:
            return Response({"detail": "Mijoz topilmadi"}, status=404)

        growth = (client.current_followers or 0) - (client.initial_followers or 0)
        data = {
            'client_name': client.name,
            'total_orders': client.total_orders,
            'total_spent': client.total_spent or 0,
            'active_tasks': client.active_tasks,
            'followers_growth': growth,
            'content_stats': {
                'pending': client.pending_plans,
                'approved': client.approved_plans,
                'published': client.published_plans,
            }
        }
        return Response(data)


class AdminDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Dashboard'])
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