from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('client', 'amount', 'method', 'is_confirmed', 'transaction_id', 'created_at')
    list_filter = ('is_confirmed', 'method', 'created_at')
    search_fields = ('client__name', 'transaction_id')
    actions = ['confirm_payments']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_confirmed:
            return ('is_confirmed', 'amount', 'client', 'method', 'transaction_id')
        return ('is_confirmed',)

    @admin.action(description="Tanlangan to'lovlarni tasdiqlash")
    def confirm_payments(self, request, queryset):
        count = 0
        for payment in queryset:
            if not payment.is_confirmed:
                payment.is_confirmed = True
                payment.save()
                count += 1
        self.message_user(request, f"{count} ta to'lov tasdiqlandi va mijozlar balansi yangilandi.")