from django.contrib.auth import get_user_model
from django.db import models


class Notification(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, unique=True)
    connect_token = models.CharField(max_length=63, null=True, unique=True)
    telegram_username = models.CharField(max_length=255, unique=True, null=True)
    chat_id = models.IntegerField(unique=True, null=True)
