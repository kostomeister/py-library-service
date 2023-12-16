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
                f"Hello there, dear reader! 📚🐝\n\n"
                f"We're excited to inform you that you've successfully created a new borrowing for '{borrowing.book_id.title}' at BuzzingPages. 📚🌟\n"
                f"Borrowing Details:\n\n"
                f"   - Borrow Date: {borrowing.borrow_date}\n"
                f"   - Expected Return Date: {borrowing.expected_return_date}\n"
                f"   - Payment Amount: {instance.money_to_pay // 100}$\n\n"
                f"To complete the process, please make a payment using the following link: {short_url}. 💳💰\n\n"
                f"Thank you for choosing BuzzingPages for your reading needs! 📖✨"
            )
            send_message(chat_id=notification.chat_id, notification_text=notification_text)
        except Notification.DoesNotExist:
            print("No such user in Telegram.")
