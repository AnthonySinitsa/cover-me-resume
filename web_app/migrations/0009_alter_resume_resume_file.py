# Generated by Django 4.2.5 on 2023-09-29 01:18

from django.db import migrations, models
import web_app.models


class Migration(migrations.Migration):
    dependencies = [
        ("web_app", "0008_coverletter_filename"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resume",
            name="resume_file",
            field=models.FileField(upload_to=web_app.models.user_directory_path),
        ),
    ]
