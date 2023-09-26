from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True) # Defines where the files will be uploaded
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username}'s Resume"

class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    third_party_url = models.URLField()
    scraped_at = models.DateTimeField(default=timezone.now)

class CoverLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    pdf_file = models.FileField(upload_to='cover_letters/', null=True, blank=True)
    generated_at = models.DateTimeField(default=timezone.now)
    filename = models.CharField(max_length=255, default='Cover_Letter')
