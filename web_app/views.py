from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ResumeUploadForm
from django.contrib.auth.decorators import login_required

class HomePageView(LoginRequiredMixin, TemplateView):
  template_name = 'home.html'

def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      return redirect('login')
  else:
    form = UserRegisterForm()
  return render(request, 'registration/register.html', {'form': form})
  
@login_required
def upload_resume(request):
  if request.method == 'POST':
    form = ResumeUploadForm(request.POST, request.FILES)
    if form.is_valid():
      resume = form.save(commit=False)
      resume.user = request.user
      resume.save()
      return redirect('home') # or wherever you want to redirect after successful upload
  else:
    form = ResumeUploadForm()
  return render(request, 'upload_resume.html', {'form': form})
