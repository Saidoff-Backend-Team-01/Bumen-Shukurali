# Generated by Django 5.0.6 on 2024-08-02 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0007_socialuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="socialuser",
            name="provider",
            field=models.CharField(
                choices=[
                    ("google", "google"),
                    ("facebook", "facebook"),
                    ("telegram", "telegram"),
                ],
                default=1,
                verbose_name="provider",
            ),
            preserve_default=False,
        ),
    ]