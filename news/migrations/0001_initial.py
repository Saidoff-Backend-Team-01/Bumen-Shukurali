# Generated by Django 5.0.8 on 2024-10-09 15:22

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("common", "0002_alter_media_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="News",
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
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "title_en",
                    models.CharField(max_length=255, null=True, verbose_name="title"),
                ),
                (
                    "title_uz",
                    models.CharField(max_length=255, null=True, verbose_name="title"),
                ),
                (
                    "title_uk",
                    models.CharField(max_length=255, null=True, verbose_name="title"),
                ),
                (
                    "title_ru",
                    models.CharField(max_length=255, null=True, verbose_name="title"),
                ),
                ("description", models.TextField(verbose_name="description")),
                (
                    "description_en",
                    models.TextField(null=True, verbose_name="description"),
                ),
                (
                    "description_uz",
                    models.TextField(null=True, verbose_name="description"),
                ),
                (
                    "description_uk",
                    models.TextField(null=True, verbose_name="description"),
                ),
                (
                    "description_ru",
                    models.TextField(null=True, verbose_name="description"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="create at"),
                ),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
            ],
            options={
                "verbose_name": "news",
                "verbose_name_plural": "news",
            },
            managers=[
                ("published", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="NewsImage",
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
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="news_images",
                        to="common.media",
                    ),
                ),
                (
                    "news",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="news_images",
                        to="news.news",
                    ),
                ),
            ],
            options={
                "verbose_name": "news image",
                "verbose_name_plural": "news images",
            },
        ),
    ]
