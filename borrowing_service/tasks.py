from django.core.serializers import serialize

from borrowing_service.models import Borrowing

from celery import shared_task
from django.utils import timezone


@shared_task
def check_borrowings_overdue():
    current_date = timezone.now().date()
    return list(
        Borrowing.objects.filter(
            expected_return_date__lt=current_date, actual_return__isnull=True
        ).values()
    )
