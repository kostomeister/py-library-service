import os

import stripe
from celery import shared_task
from .models import Payment
from notifications.messages import notify_invalid_session
from .stripe_helper import check_session_status

stripe.api_key = os.environ.get("STRIPE_SECRET_API_KEY")


@shared_task
def check_and_notify_expired_sessions():
    sessions_to_check = Payment.objects.filter(status=Payment.StatusChoices.PENDING)
    for session in sessions_to_check:
        if check_session_status(session.session_id):
            session.status = Payment.StatusChoices.EXPIRED
            session.save()
            notify_invalid_session(session.borrowing.user_id)
