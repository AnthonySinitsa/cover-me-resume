from django.contrib import admin
from .models import CoverLetter

@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'generated_at'] 
