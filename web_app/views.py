import json
import openai
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ResumeUploadForm
from django.contrib.auth.decorators import login_required
from .models import Resume
from django.http import JsonResponse
from django.conf import settings
from .utils.pdf_utils import extract_text_from_pdf


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


def get_user_resume_as_text(resume_file_path):
  return extract_text_from_pdf(resume_file_path)


@login_required
def generate_cover_letter(request, job_index):
  # Load the jobs from jobs.json
  with open('web_app/scrapers/indeed_scraper/results/jobs.json', 'r') as file:
    jobs = json.load(file)
  
  # Get the selected job using the job_index
  selected_job = jobs[job_index]
  job_description = selected_job["description"]

  # Fetch the user's resume and extract its text.
  try:
    resume = Resume.objects.filter(user=request.user).order_by('-uploaded_at').first()
    if not resume:
      raise ValueError("No resume found for this user.")
    resume_text = get_user_resume_as_text(resume.resume_file.path)
  except ValueError as e:
    # Handle the error, e.g., by returning an error message to the user.
    error_message = str(e)
    return render(request, 'error_page.html', {'error_message': error_message})

  # Use ChatGPT to generate the cover letter
  openai_api_key = "OPENAI_API_KEY"  # Ideally, fetch this from your .env or settings
  headers = {
      "Authorization": f"Bearer {openai_api_key}",
      "Content-Type": "application/json",
  }
  prompt_text = f"Given the job description: '{job_description}' and the resume: '{resume_text}', generate a suitable cover letter."
  data = {
      "prompt": prompt_text,
      "max_tokens": 500  # Just an example, adjust as needed.
  }
  response = requests.post("https://api.openai.com/v1/engines/text-davinci-002/completions", headers=headers, data=json.dumps(data))
  response_data = response.json()

  # Error checks
  if 'choices' not in response_data or not response_data['choices'] or 'text' not in response_data['choices'][0]:
      error_message = "Failed to generate the cover letter. Please try again."
      return render(request, 'error_page.html', {'error_message': error_message})

  cover_letter = response_data['choices'][0]['text'].strip()

  # Render the cover letter on a new page or however you wish to display it.
  return render(request, 'cover_letter_page.html', {'cover_letter': cover_letter})
