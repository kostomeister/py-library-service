# Generated by Django 4.0.4 on 2023-12-14 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_service', '0001_initial'),
        ('borrowing_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='borrowing',
            options={'ordering': ('-borrow_date',)},
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='book_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowings', to='book_service.book'),
        ),
    ]
