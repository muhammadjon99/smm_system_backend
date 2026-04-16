from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentPlanViewSet

router = DefaultRouter()
router.register(r'', ContentPlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]