# Generated by Django 4.1.6 on 2023-08-16 09:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="country_code",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]