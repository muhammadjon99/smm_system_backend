from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum


def check_order_limits(client, service):
    current_month = timezone.now().month
    current_year = timezone.now().year
    s_type = getattr(service, 'service_type', None)
    if not s_type:
        return
    client_limit = getattr(client, f"{s_type}_limit", 0)
    used_count = client.orders.filter(
        service__service_type=s_type,
        created_at__month=current_month,
        created_at__year=current_year,
        status__in=['pending', 'processing', 'completed']
    ).aggregate(total=Sum('quantity'))['total'] or 0
    if used_count >= client_limit:
        raise ValidationError(
            f"Limit tugagan! Sizning oylik {s_type} limitingiz: {client_limit} ta. "
            f"Shu oyda foydalanilgan: {used_count} ta."
        )