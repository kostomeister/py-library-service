import os
import requests
import pyshorteners

from notifications.models import Notification


def handle_notification_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Notification.DoesNotExist:
            print("This user is not registered on Telegram")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    return wrapper


def send_message(chat_id, notification_text):
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    return requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}"
                        f"/sendMessage?chat_id={chat_id}&text={notification_text}")


@handle_notification_exception
def notify_overdue_borrowing(user_id):
    notification = Notification.objects.get(user_id=user_id)
    text = (
        f"Hello {notification.telegram_username}! 📚🌟\n\n"
        f"We hope this message finds you well. 😊 It looks like there's a small reminder about your recent borrowing at BuzzingPages:\n"
        f"We kindly request you to return the book at your earliest convenience."
        f"If you've already returned it, please accept our apologies for any inconvenience.\n\n"
        f"Thank you for your understanding and prompt attention! 🙏📚"
    )
    return send_message(chat_id=notification.chat_id, notification_text=text)


@handle_notification_exception
def send_user_payment_message(instance):
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(instance.session_url)

    borrowing = instance.borrowing
    notification = Notification.objects.get(user_id=borrowing.user_id)

    notification_text = (
        f"Hello there, dear reader! 📚🐝\n\n"
        f"We're excited to inform you that you've "
        f"successfully created a new borrowing for '{borrowing.book_id.title}' at BuzzingPages. 📚🌟\n"
        f"Borrowing Details:\n\n"
        f"   - Borrow Date: {borrowing.borrow_date}\n"
        f"   - Expected Return Date: {borrowing.expected_return_date}\n"
        f"   - Payment Amount: {instance.money_to_pay}$\n\n"
        f"To complete the process, please make a payment using the following link: {short_url}. 💳💰\n\n"
        f"Thank you for choosing BuzzingPages for your reading needs! 📖✨"
    )

    return send_message(chat_id=notification.chat_id, notification_text=notification_text)


@handle_notification_exception
def send_admin_borrowing_message(instance):
    admin_chat_id = "-4085174893"

    notification_text = (
        f"Hello Admins! 📚👋\n\n"
        f"A new borrowing has been created for the "
        f"book '{instance.book_id.title}' at BuzzingPages. 📚📅\n"
        f"Borrowing Details:\n\n"
        f"   - User: {instance.user_id.email}\n"
        f"   - Borrow Date: {instance.borrow_date}\n"
        f"   - Expected Return Date: {instance.expected_return_date}\n\n"
        f"Thank you for your attention! ✨"
    )

    return send_message(chat_id=admin_chat_id, notification_text=notification_text)


@handle_notification_exception
def notify_invalid_session(user_id):
    notification = Notification.objects.get(user_id=user_id)
    text = (f"Hi, {notification.telegram_username}! 😕\n\n"
            f"We're sorry, but it seems that your session is expired. "
            f"Please review and try again or contact our support for assistance.")
    return send_message(chat_id=notification.chat_id, notification_text=text)


@handle_notification_exception
def successful_payment_message(borrowing):
    notification = Notification.objects.get(user=borrowing.user_id)
    notification_text = (
        f"Hello dear {notification.telegram_username}! 🎉💳\n\n"
        f"We're thrilled to inform you that your payment for the borrowing of '{borrowing.book_id.title}' at BuzzingPages was successful. 📚💰\n"
        f"Borrowing Details:\n\n"
        f"   - Borrow Date: {borrowing.borrow_date}\n"
        f"   - Expected Return Date: {borrowing.expected_return_date}\n\n"
        f"Thank you for completing the payment and choosing BuzzingPages for your reading needs! 📖✨\n\n"
        f"If you have any questions or need assistance, feel free to reach out to us. Happy reading!"
    )
    return send_message(chat_id=notification.chat_id, notification_text=notification_text)


@handle_notification_exception
def successful_fine_payment_message(borrowing):
    notification = Notification.objects.get(user=borrowing.user_id)
    notification_text = (
        f"Hello {notification.telegram_username}! 🎉💳\n\n"
        f"Great news! You've successfully paid the fine for the late return of '{borrowing.book_id.title}' at BuzzingPages. 📚💰\n"
        f"Thank you for addressing the fine and choosing BuzzingPages for your reading needs! 📖✨\n\n"
        f"If you have any questions or need further assistance, feel free to reach out. Happy reading!"
    )
    return send_message(chat_id=notification.chat_id, notification_text=notification_text)
