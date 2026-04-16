from rest_framework import serializers
from .models import ContentPlan

class ContentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentPlan
        fields = '__all__'