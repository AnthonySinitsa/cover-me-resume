# Generated by Django 4.2.5 on 2023-09-29 06:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("web_app", "0010_job"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="job",
            name="link",
        ),
        migrations.AlterField(
            model_name="job",
            name="post_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
