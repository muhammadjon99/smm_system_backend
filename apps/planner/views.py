from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import ContentPlan
from .serializers import ContentPlanSerializer


class ContentPlanViewSet(viewsets.ModelViewSet):
    queryset = ContentPlan.objects.all().order_by('post_date')
    serializer_class = ContentPlanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'post_date', 'status']

    def get_queryset(self):
        queryset = ContentPlan.objects.all()
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        if month and year:
            queryset = queryset.filter(post_date__month=month, post_date__year=year)
        return queryset