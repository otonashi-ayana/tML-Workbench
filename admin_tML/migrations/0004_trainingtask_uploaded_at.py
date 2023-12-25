# Generated by Django 4.1.12 on 2023-12-24 13:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("admin_tML", "0003_trainingtask_delete_mlmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainingtask",
            name="uploaded_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]