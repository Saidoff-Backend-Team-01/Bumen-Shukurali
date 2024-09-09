from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("common", "0001_initial"),
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
                (
                    "image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="news",
                        to="common.media",
                    ),
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
    ]
