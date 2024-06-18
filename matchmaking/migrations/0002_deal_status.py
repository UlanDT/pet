# Generated by Django 4.2.3 on 2024-05-18 03:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("matchmaking", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="deal",
            name="status",
            field=models.CharField(
                choices=[
                    ("open", "Open"),
                    ("closed", "Closed"),
                    ("in progress", "In Progress"),
                ],
                default="open",
                max_length=20,
            ),
        ),
    ]
