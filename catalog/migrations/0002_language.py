# Generated by Django 4.1.4 on 2022-12-31 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
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
                    "name",
                    models.CharField(
                        default="English",
                        help_text="Enter the book's natural language (e.g. Spanish, French, Japanese etc.)",
                        max_length=200,
                    ),
                ),
            ],
        ),
    ]
