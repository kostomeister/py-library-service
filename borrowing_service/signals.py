from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowing_service.models import Borrowing
from notifications.models import Notification
from payment_service.models import Payment
from notifications.messages import (
    send_user_payment_message,
    send_admin_borrowing_message
)


@receiver(post_save, sender=Payment)
def send_payment_message_user(sender, instance, created, **kwargs):
    """
    Signal receiver function triggered after a Payment object is saved.

    This function sends a notification message to the user via Telegram
    when a new Payment object is created. It fetches borrowing details related
    to the payment, generates a short payment URL using pyshorteners, and sends
    a formatted notification message including borrowing information and payment link.

    Args:
    - sender: The sender of the signal.
    - instance: The instance of the Payment object.
    - created (bool): Indicates if the Payment object is newly created.
    - kwargs: Additional keyword arguments.

    Returns:
    - None
    """
    if created:
        if instance.type == "Payment":
            try:
                send_user_payment_message(instance)
            except Notification.DoesNotExist:
                print("No such user in Telegram.")


@receiver(post_save, sender=Borrowing)
def send_borrow_message_admin(sender, instance, created, **kwargs):
    if created:
        send_admin_borrowing_message(instance)
