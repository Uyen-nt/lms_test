# Generated by Django 5.0.9 on 2024-09-19 03:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("module_group", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Module",
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
                ("module_name", models.CharField(max_length=255)),
                ("module_url", models.CharField(max_length=255)),
                ("icon", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "module_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="modules",
                        to="module_group.modulegroup",
                    ),
                ),
            ],
        ),
    ]
