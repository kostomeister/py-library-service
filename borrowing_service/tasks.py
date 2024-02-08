from borrowing_service.models import Borrowing

from celery import Celery
from celery import shared_task
from django.utils import timezone

from notifications.messages import notify_overdue_borrowing


app = Celery("tasks", backend="redis://localhost", broker="redis://localhost")


@shared_task
def check_borrowings_overdue():
    """
    Asynchronous task to check for overdue borrowings and notify users.

    This function retrieves borrowings with an `expected_return_date` in the past
    and no actual return date set. It then notifies users about these overdue borrowings.
    """
    current_date = timezone.now().date()
    borrowings = list(
        Borrowing.objects.filter(
            expected_return_date__lt=current_date, actual_return__isnull=True
        ).values()
    )
    for borrowing in borrowings:
        notify_overdue_borrowing(borrowing["user_id_id"])
