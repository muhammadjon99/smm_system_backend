from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'insta_username', 'created_at', 'address', 'logo', 'insta_password', 'current_followers', 'monthly_budget', )
    search_fields = ('name', 'phone', 'insta_username')