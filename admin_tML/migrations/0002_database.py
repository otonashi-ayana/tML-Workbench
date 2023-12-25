# Generated by Django 4.1.12 on 2023-12-21 12:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_tML", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Database",
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
                ("name", models.CharField(max_length=100)),
                ("upload", models.FileField(upload_to="databases/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
