# Generated by Django 4.0.4 on 2023-12-14 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("borrowing_service", "0002_alter_borrowing_options_alter_borrowing_book_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Pending", "Pending"), ("Paid", "Paid")],
                        max_length=20,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("Payment", "Payment"), ("Fine", "Fine")],
                        max_length=20,
                    ),
                ),
                ("session_url", models.URLField()),
                ("session_id", models.CharField(max_length=255)),
                ("money_to_pay", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "borrowing",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="borrowing_service.borrowing",
                    ),
                ),
            ],
        ),
    ]