from django.db.models.signals import post_save
from django.dispatch import receiver
import pyshorteners

from notifications.models import Notification
from payment_service.models import Payment
from .models import Borrowing
from notifications.messages import send_message


@receiver(post_save, sender=Payment)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            borrowing = instance.borrowing
            notification = Notification.objects.get(user_id=borrowing.user_id)

            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(instance.session_url)

            notification_text = (
                f"Hello, you сreated a new borrowing of a '{borrowing.book_id.title}'\n"
                f"You should pay for it first: {short_url}"
            )
            send_message(chat_id=notification.chat_id, notification_text=notification_text)
        except Notification.DoesNotExist:
            print("no such user in tg")
