from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .models import ContentPlan
from .serializers import ClientDashboardSerializer


@extend_schema(tags=['Planner'])
class ContentPlanViewSet(viewsets.ModelViewSet):
    queryset = ContentPlan.objects.all().select_related('client', 'order').order_by('post_date')
    serializer_class = ClientDashboardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'post_date', 'status']
    def get_queryset(self):
        queryset = ContentPlan.objects.all().select_related('client', 'order')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if month and year:
            queryset = queryset.filter(post_date__month=month, post_date__year=year)
        return queryset.order_by('post_date')