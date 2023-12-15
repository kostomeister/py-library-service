from django.contrib.auth import get_user_model
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    connect_token = models.CharField(max_length=63, null=True)
