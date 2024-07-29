# Generated by Django 5.0.6 on 2024-07-10 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("common", "0002_alter_media_options_alter_media_file"),
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
                ("description", models.TextField(verbose_name="description")),
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="create at"),
                ),
                (
                    "image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="common.media",
                    ),
                ),
            ],
            options={
                "verbose_name": "news",
                "verbose_name_plural": "news",
            },
        ),
    ]