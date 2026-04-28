from django.contrib import admin
from .models import Order
from import_export.admin import ExportMixin

@admin.register(Order)
class OrderAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('client', 'service', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('total_price',)