# Generated by Django 4.2.14 on 2024-08-09 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_auth_type_delete_socialuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Birthday Data'),
        ),
    ]
