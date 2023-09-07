from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ResumeUploadForm
from django.contrib.auth.decorators import login_required
from .models import Resume
import json

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

@login_required
def profile(request):
  user_resumes = Resume.objects.filter(user=request.user)
  context = {'resumes': user_resumes}
  return render(request, 'profile.html', context)

def job_search(request):
  if request.method == "POST":
    job_title = request.POST.get('job_title')
    job_location = request.POST.get('job_location')

    # Run the scraper
    from scrapers.indeed_scraper import run
    run.scrape_jobs(job_title, job_location)

    # Redirect to results page after scraping
    return redirect('job_results')
  return render(request, 'job_search.html')

def job_results(request):
  # Step 1: Reading the JSON File
  with open('web_app/scrapers/indeed_scraper/results/jobs.json', 'r') as file:
    job_data = json.load(file)

  # Step 2: Extracting the Relevant Data
  jobs_list = []
  for job in job_data:
    job_info = {
      "description": job["description"],
      "companyName": job["companyName"],
      "companyOverviewLink": job["companyOverviewLink"]
    }
    jobs_list.append(job_info)

  # Step 3: Passing the Data to the Template
  return render(request, 'job_results.html', {'jobs': jobs_list})