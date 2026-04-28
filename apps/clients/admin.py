from django.contrib import admin
from django import forms
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'video_limit',
        'post_limit',
        'total_paid',
        'created_at'
    )
    list_editable = ('video_limit', 'post_limit')
    search_fields = ('name', 'phone', 'insta_username')
    list_filter = ('created_at',)
    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('name', 'phone', 'address', 'logo')
        }),
        ('Instagram Sozlamalari', {
            'classes': ('collapse',),
            'fields': ('insta_username', 'insta_password', 'initial_followers', 'current_followers'),
            'description': 'Mijoz maxfiy ma\'lumotlari (Ko\'rish uchun "Show" tugmasini bosing)'
        }),
        ('Limitlar va Byudjet', {
            'fields': ('video_limit', 'post_limit', 'story_limit', 'reels_limit', 'monthly_budget', 'total_paid')
        }),
    )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'insta_password' in form.base_fields:
            form.base_fields['insta_password'].widget = forms.PasswordInput(render_value=False)
            form.base_fields['insta_password'].help_text = "Xavfsizlik uchun parol yashirilgan."
        return form