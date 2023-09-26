from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Resume, CoverLetter

class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()  # Optionally add an email field

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class ResumeUploadForm(forms.ModelForm):
  class Meta:
    model = Resume
    fields = ['resume_file']
    
class EditCoverLetterForm(forms.ModelForm):
  class Meta:
    model = CoverLetter
    fields = ['content']