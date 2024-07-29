# Generated by Django 5.0.6 on 2024-07-15 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0003_contactwithus"),
    ]

    operations = [
        migrations.CreateModel(
            name="FAQ",
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
                ("question", models.TextField()),
                ("answer", models.TextField()),
            ],
            options={
                "verbose_name": "FAQ",
            },
        ),
    ]