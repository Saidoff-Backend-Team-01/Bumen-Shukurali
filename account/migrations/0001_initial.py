# Generated by Django 5.1.1 on 2024-09-29 07:13

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="IntroQuestion",
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
                    "title",
                    models.CharField(
                        max_length=200, verbose_name="Introduction question"
                    ),
                ),
                ("more_info", models.TextField(verbose_name="More info")),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("username", models.CharField(blank=True, max_length=123, null=True)),
                (
                    "birth_date",
                    models.DateField(blank=True, null=True, verbose_name="birth_date"),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        verbose_name="email address",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="phone number",
                    ),
                ),
                (
                    "father_name",
                    models.CharField(
                        blank=True,
                        max_length=120,
                        null=True,
                        verbose_name="father name",
                    ),
                ),
                (
                    "auth_type",
                    models.CharField(
                        choices=[
                            ("GOOGLE", "Google Account"),
                            ("FACEBOOK", "Facebook Account"),
                            ("TELEGRAM", "Telegram Account"),
                            ("WITH EMAIL", "Email Auth"),
                            ("WITH PHONE", "Phone Auth"),
                        ],
                        default="WITH PHONE",
                        max_length=244,
                        verbose_name="auth type",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("male", "Male"), ("female", "Female")],
                        null=True,
                        verbose_name="gender",
                    ),
                ),
                (
                    "telegram_id",
                    models.CharField(
                        blank=True, max_length=55, null=True, verbose_name="telegram id"
                    ),
                ),
                (
                    "device_id",
                    models.CharField(
                        blank=True, max_length=244, null=True, verbose_name="device id"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "photo",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="photo",
                        to="common.media",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
        migrations.CreateModel(
            name="Groups",
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
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "users",
                    models.ManyToManyField(
                        related_name="user_groups", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "Group",
                "verbose_name_plural": "Groups",
            },
        ),
        migrations.CreateModel(
            name="IntroQuestionAnswer",
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
                ("text", models.TextField(verbose_name="Answer")),
                (
                    "intro_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.introquestion",
                        verbose_name="Question",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SocialUser",
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
                    "social_user_id",
                    models.IntegerField(blank=True, null=True, verbose_name="user id"),
                ),
                (
                    "provider",
                    models.CharField(
                        choices=[
                            ("google", "google"),
                            ("facebook", "facebook"),
                            ("telegram", "telegram"),
                        ],
                        max_length=255,
                        verbose_name="provider",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "extra_data",
                    models.JSONField(default=dict, verbose_name="extra data"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserIntroQuestion",
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
                ("is_marked", models.BooleanField(default=True)),
                (
                    "answer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="account.introquestionanswer",
                        verbose_name="Answer",
                    ),
                ),
                (
                    "intro_question",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.introquestion",
                        verbose_name="Question",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserMessage",
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
                ("message", models.TextField(verbose_name="Message")),
                (
                    "file",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="common.media",
                        verbose_name="File",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.groups",
                        verbose_name="Group",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "User's message",
                "verbose_name_plural": "User's messages",
            },
        ),
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
                ("is_used", models.BooleanField(default=False, verbose_name="is_used")),
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
