# Generated by Django 4.0.4 on 2023-12-15 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_alter_notification_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='telegram_username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
