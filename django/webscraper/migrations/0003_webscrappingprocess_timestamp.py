# Generated by Django 4.1.7 on 2023-05-11 19:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("webscraper", "0002_webscrappingprocess"),
    ]

    operations = [
        migrations.AddField(
            model_name="webscrappingprocess",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
