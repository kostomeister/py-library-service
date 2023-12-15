import os
import requests

from notifications.models import Notification

BOT_TOKEN = os.environ.get("BOT_TOKEN")


def send_message(chat_id, notification_text):
    return requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}"
        f"/sendMessage?chat_id={chat_id}"
        f"&text={notification_text}")


def notify_overdue_borrowing(user_id):
    notification = Notification.objects.get(user_id=user_id)
    text = (f"Hi, {notification.telegram_username} your borrowing is overdue. "
            f"Please return it as soon as possible.")
    return send_message(notification.chat_id, text)
