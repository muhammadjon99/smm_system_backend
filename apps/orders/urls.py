from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,DashboardAnalyticsView

router = DefaultRouter()
router.register(r'', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/dashboard/', DashboardAnalyticsView.as_view(), name='analytics-dashboard'),
]