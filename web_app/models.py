from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_text = models.TextField()
    uploaded_at = models.DateTimeField(default=timezone.now)

class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    third_party_url = models.URLField()
    scraped_at = models.DateTimeField(default=timezone.now)

class CoverLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    content = models.TextField()
    generated_at = models.DateTimeField(default=timezone.now)
