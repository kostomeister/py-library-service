import os
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")


def send_message(chat_id, notification_text):
    return requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}"
        f"/sendMessage?chat_id={chat_id}"
        f"&text={notification_text}")
