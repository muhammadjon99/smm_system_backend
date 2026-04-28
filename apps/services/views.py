from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from django.db.models import Count
from .models import Service
from .serializers import ServiceSerializer

@extend_schema(tags=['Services'])
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().annotate(
        orders_count=Count('orders')
    ).order_by('name')
    serializer_class = ServiceSerializer