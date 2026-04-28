from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'method', 'is_confirmed', 'created_at')
    list_filter = ('is_confirmed', 'method', 'created_at')
    search_fields = ('client__name', 'transaction_id')
    actions = ['confirm_payments']

    @admin.action(description="Tanlangan to'lovlarni tasdiqlash")
    def confirm_payments(self, request, queryset):
        for payment in queryset:
            if not payment.is_confirmed:
                payment.is_confirmed = True
                payment.save()
        self.message_user(request, "Tanlangan to'lovlar tasdiqlandi va mijozlar balansi yangilandi.")