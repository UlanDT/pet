# Generated by Django 4.2.3 on 2024-05-18 04:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="balance",
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20),
            preserve_default=False,
        ),
    ]
