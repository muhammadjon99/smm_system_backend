from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('total_price',) # Bu o'zi hisoblanadi