import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Media",
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
                    "type",
                    models.CharField(
                        choices=[
                            ("image", "image"),
                            ("video", "video"),
                            ("audio", "audio"),
                            ("file", "file"),
                            ("music", "music"),
                        ],
                        max_length=50,
                        verbose_name="type",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="media_files",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=[
                                    "png",
                                    "jpg",
                                    "jpeg",
                                    "gif",
                                    "mp4",
                                    "mp3",
                                ]
                            )
                        ],
                        verbose_name="file",
                    ),
                ),
            ],
            options={
                "verbose_name": "Media",
                "verbose_name_plural": "Media",
            },
        ),
    ]
