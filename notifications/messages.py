import os
import requests

from notifications.models import Notification


def send_message(chat_id, notification_text):
    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    return requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}"
        f"/sendMessage?chat_id={chat_id}&text={notification_text}"
    )


def notify_overdue_borrowing(user_id):
    """
    Notifies a user about an overdue borrowing via Telegram.

    Retrieves the user's id and sends a notification message about the overdue borrowing.

    Args:
    - user_id (int): The ID of the user.

    Returns:
    - Response: Response object from the send_message function call.
    """
    notification = Notification.objects.get(user_id=user_id)
    text = (
        f"Hi, {notification.telegram_username} your borrowing is overdue. "
        f"Please return it as soon as possible."
    )
    return send_message(notification.chat_id, text)


def send_admin_borrowing_message():
    return None


def send_user_payment_message():
    return None