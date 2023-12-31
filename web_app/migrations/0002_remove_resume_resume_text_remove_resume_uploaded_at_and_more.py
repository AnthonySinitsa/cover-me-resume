# Generated by Django 4.2 on 2023-09-06 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='resume_text',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='uploaded_at',
        ),
        migrations.AddField(
            model_name='resume',
            name='resume_file',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
