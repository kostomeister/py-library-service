import asyncio
import logging
import os
import sys
import asyncio
import logging

import requests
from aiogram.utils.markdown import *
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from django.conf import settings
from django.apps import apps


conf = {
    "SECRET_KEY": "django-insecure-kvk=ah*jq3^3479#u40#ioz*b5+c5f0e-8hktlsaamtkdhz88a",
    "INSTALLED_APPS": [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "rest_framework",
        "rest_framework_simplejwt",
        "user",
        "book_service",
        "notifications",
        "borrowing_service",
        "payment_service",
    ],
    "DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    },
    "TIME_ZONE": "UTC",
}

settings.configure(**conf)
apps.populate(settings.INSTALLED_APPS)

from notifications.models import Notification
from borrowing_service.models import Borrowing
from book_service.models import Book


load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Handles the /start command to create a user notification in the Django database
    and sends a welcome message to the user on Telegram.
    Args:
    - message (Message): The message from the user.

    """
    text = message.text
    user_id = int(text[text.find("userid") + 6:])
    user_token = text[7:text.find("userid")]

    await (sync_to_async(Notification.objects.create)
           (user_id=user_id,
            connect_token=user_token,
            telegram_username=message.from_user.username,
            chat_id=message.chat.id))

    await (sync_to_async(Notification.objects.get)(user_id=user_id))

    await message.answer(f"Hi, {hbold(message.from_user.username)}! \n\n"
                         f"I will help you to keep track "
                         f"of your borrowings in our library. \n\n"
                         f"{hbold('Happy reading!')} \U0001F970")


@dp.message(Command("myborrowings"))
async def get_borrowings_handler(message: Message) -> None:
    """
    Handles the /myborrowings command to fetch information about the user's current
    borrowings and sends a message to the user with this information.

    Args:
    - message (Message): The message from the user.
    """
    notification = await sync_to_async(Notification.objects.get)(
        telegram_username=message.from_user.username
    )

    user_id = notification.user_id

    user_borrowings = await (sync_to_async(Borrowing.objects.filter)
                             (user_id=user_id))

    message_text = "Here are all of your current borrowings: \n"

    for borrowing in await sync_to_async(list)(user_borrowings):
        book_id = await sync_to_async(lambda: borrowing.book_id_id)()

        book = await sync_to_async(Book.objects.get)(id=book_id)
        return_date = await sync_to_async(lambda: borrowing.expected_return_date)()

        message_text += f"{str(book)} - expected to return {return_date}\n"

    await message.answer(message_text)


async def main() -> None:
    """
    The main function initializing and starting the Telegram bot.
    """
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
