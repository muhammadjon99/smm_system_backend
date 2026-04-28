from django.core.exceptions import ValidationError
from django.db.models import Sum


def check_order_limits(client, service):
    s_type = service.service_type
    limit_map = {
        'video': client.video_limit,
        'post': client.post_limit,
        'story': client.story_limit,
        'reels': client.reels_limit
    }
    if s_type in limit_map:
        user_limit = limit_map[s_type]
        if user_limit > 0:
            used_data = client.orders.filter(
                service__service_type=s_type
            ).exclude(
                status='cancelled'
            ).aggregate(total=Sum('quantity'))
            used_count = used_data['total'] or 0
            if used_count >= user_limit:
                raise ValidationError(
                    f"{service.get_service_type_display()} limiti tugagan. "
                    f"Maksimal: {user_limit}, ishlatilgan: {used_count}"
                )