from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db import models
from django.conf import settings

def user_directory_path(instance, filename):
    # This will save the file under <user_id>/resume.pdf
    return f'{instance.user.id}/resume.pdf'

class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to=user_directory_path) # Defines where the files will be uploaded     null=True, blank=True
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

class Job(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    company_overview_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title