# Generated by Django 5.0.9 on 2024-09-18 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ("course_name", models.CharField(max_length=255)),
                ("course_description", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "course",
            },
        ),
    ]
