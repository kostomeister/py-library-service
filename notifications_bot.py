import asyncio
import logging
import os
import sys

import requests
from aiogram.utils.markdown import *
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand

from django.conf import settings
from django.apps import apps
conf = {
    "SECRET_KEY":
        'django-insecure-kvk=ah*jq3^3479#u40#ioz*b5+c5f0e-8hktlsaamtkdhz88a',
    "INSTALLED_APPS": [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        "rest_framework",
        "rest_framework_simplejwt",
        "user",
        "book_service",
        "notifications",
    ],
    "DATABASES": {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    'TIME_ZONE': 'UTC',
}

settings.configure(**conf)
apps.populate(settings.INSTALLED_APPS)

from notifications.models import Notification


load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = message.text
    user_id = text[text.find("userid") + 6:]
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
                         f"{hbold("Happy reading!")} \U0001F970")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
