# Generated by Django 5.0.6 on 2024-07-29 15:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0003_alter_user_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserOtpCode",
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
                ("code", models.CharField(max_length=6)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("register", "Register"),
                            ("reset_password", "Reset Password"),
                        ],
                        max_length=20,
                        verbose_name="type",
                    ),
                ),
                (
                    "expires_in",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="expires_in"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is_active"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]