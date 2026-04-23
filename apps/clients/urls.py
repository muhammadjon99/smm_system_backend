from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet,AdminDashboardAPIView

router = DefaultRouter()
router.register(r'', ClientViewSet, basename='client')

urlpatterns = [
    path('', include(router.urls)),
    path('admin-dashboard/', AdminDashboardAPIView.as_view(), name='admin-dashboard'),
]