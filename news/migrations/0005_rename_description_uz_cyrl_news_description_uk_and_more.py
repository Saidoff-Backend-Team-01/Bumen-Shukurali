# Generated by Django 5.1.1 on 2024-10-04 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0004_news_description_uz_cyrl_news_title_uz_cyrl"),
    ]

    operations = [
        migrations.RenameField(
            model_name="news",
            old_name="description_uz_cyrl",
            new_name="description_uk",
        ),
        migrations.RenameField(
            model_name="news",
            old_name="title_uz_cyrl",
            new_name="title_uk",
        ),
    ]
