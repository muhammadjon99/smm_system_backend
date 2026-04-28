from django.contrib import admin
from django import forms
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'insta_username',
        'current_followers',
        'monthly_budget',
        'created_at'
    )
    search_fields = ('name', 'phone', 'insta_username')
    list_filter = ('created_at',)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'insta_password' in form.base_fields:
            form.base_fields['insta_password'].widget = forms.PasswordInput(render_value=True)
            form.base_fields[
                'insta_password'].help_text = "Mijozning Instagram paroli shifrlangan holatda kiritilishi tavsiya etiladi."
        return form