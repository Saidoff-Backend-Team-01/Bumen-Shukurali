# Generated by Django 5.0.6 on 2024-09-09 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supject", "0002_alter_club_description_alter_club_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usertotaltestresult",
            name="percentage",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]