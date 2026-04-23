from django.core.exceptions import ValidationError
from django.utils import timezone

def check_order_limits(client, service):
    current_month = timezone.now().month
    orders_count = client.orders.filter(
        service=service,
        created_at__month=current_month,
        status__in=['pending', 'processing', 'completed']
    ).count()

    if orders_count >= service.video_limit:
        raise ValidationError(
            f"Limit tugagan: {service.video_limit} ta."
        )