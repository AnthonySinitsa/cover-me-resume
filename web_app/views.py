import os
import json
import openai
import requests
import pdfkit
import asyncio
from io import BytesIO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import UserRegisterForm, ResumeUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Resume, CoverLetter
from django.http import JsonResponse, FileResponse, HttpResponse
from django.conf import settings
from .utils.pdf_utils import extract_text_from_pdf
from .utils.text_utils import strip_html_tags
from wsgiref.util import FileWrapper
from django.core.files.base import ContentFile
from datetime import datetime
from web_app.scrapers.indeed_scraper.run import run
from .tasks import run_scraper
from celery.result import AsyncResult


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
      # Check if the user already has a resume
      existing_resume = Resume.objects.filter(user=request.user).first()
      
      if existing_resume:
        # If a resume exists, delete the old file from storage
        existing_resume.resume_file.delete()
        
        # Update the resume file with the new one
        existing_resume.resume_file = form.cleaned_data['resume_file']
        existing_resume.save()
      else:
        # If no resume exists, create a new Resume object
        resume = form.save(commit=False)
        resume.user = request.user
        resume.save()
            
      return redirect('home')  # or wherever you want to redirect after successful upload
  else:
    form = ResumeUploadForm()
  return render(request, 'upload_resume.html', {'form': form})



@login_required
def profile(request):
  resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
  cover_letters = CoverLetter.objects.filter(user=request.user).order_by('-generated_at')
  return render(request, 'profile.html', {'resumes': resumes, 'cover_letters': cover_letters})


def job_search(request):
  if request.method == "POST":
    job_title = request.POST.get('job_title')
    job_location = request.POST.get('location')

    # Send the scraping task to Celery
    task = run_scraper.delay(job_title, job_location)

    # Render the loading page
    return render(request, 'loading.html', {'task_id': task.id})
  return render(request, 'job_search.html')


def job_results(request, task_id=None):
  if task_id:
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
    return render(request, 'job_results.html', {'jobs': jobs_list, 'task_id': task_id})
  return render(request, 'error_page.html', {'message': 'No task ID provided.'})



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
    resume_content = resume.resume_file.read()
    resume_text = extract_text_from_pdf(resume_content)
  except ValueError as e:
    # Handle the error, e.g., by returning an error message to the user.
    error_message = str(e)
    return render(request, 'error_page.html', {'error_message': error_message})

  # Use ChatGPT to generate the cover letter
  openai_api_key = settings.OPENAI_API_KEY
  headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json",
  }
  prompt_text = f"I want you to act as a cover letter writer. Given the job description: '{job_description}' and the resume: '{resume_text}', generate a suitable cover letter."
  data = {
    "prompt": prompt_text,
    "max_tokens": 1000  # Just an example, adjust as needed.
  }
  response = requests.post("https://api.openai.com/v1/engines/text-davinci-002/completions", headers=headers, data=json.dumps(data))

  # Check the response status
  if response.status_code != 200:
    # Log the error content and display an error message to the user
    print(f"OpenAI API Error: {response.status_code} - {response.text}")
    error_message = "Failed to generate the cover letter due to an API error. Please try again."
    return render(request, 'error_page.html', {'error_message': error_message})

  response_data = response.json()

  # Error checks
  if 'choices' not in response_data or not response_data['choices'] or 'text' not in response_data['choices'][0]:
    error_message = "Failed to generate the cover letter. Please try again."
    return render(request, 'error_page.html', {'error_message': error_message})

  cover_letter = response_data['choices'][0]['text'].strip()
  cleaned_cover_letter = strip_html_tags(cover_letter) # THIS ISN'T BEING USED, BUT MAYBE NEED FOR LATER

  # Render the cover letter on a new page or however you wish to display it.
  return render(request, 'cover_letter_page.html', {'cover_letter': cover_letter})


@login_required
def download_cover_letter(request, cover_letter_id=None):
  # If cover_letter_id is provided, it means we are serving an already-saved PDF
  if cover_letter_id:
    cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id)
    pdf = cover_letter.pdf_file.read()

    # Serve the PDF as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cover_letter.pdf_file.name}"'
    return response

  # If cover_letter_id is not provided, we generate the PDF on-the-fly
  cover_letter_text = request.POST.get('cover_letter_text')

  # Retrieve the custom filename from POST data
  custom_filename = request.POST.get('cover_letter_filename', 'Cover_Letter')

  # Convert newline characters to <br> for proper HTML rendering
  cover_letter_html = cover_letter_text.replace('\n', '<br>')

  # Convert the HTML to PDF
  pdf = pdfkit.from_string(cover_letter_html, False)

  # Save the generated PDF to the database with the custom filename
  cover_letter_record = CoverLetter(
    user=request.user, 
    pdf_file=ContentFile(pdf, name=f"{custom_filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
  )

  cover_letter_record.save()

  # Serve the generated PDF as a response using the custom filename
  response = HttpResponse(pdf, content_type='application/pdf')
  response['Content-Disposition'] = f'attachment; filename="{custom_filename}.pdf"'
  return response


@login_required
def delete_cover_letter(request, letter_id):
  cover_letter = get_object_or_404(CoverLetter, id=letter_id, user=request.user)
  cover_letter.delete()
  return redirect('profile')


def check_task_status(request, task_id):
  task = AsyncResult(task_id)
  response_data = {
    'status': task.status,
    'result': task.result,
  }
  return JsonResponse(response_data)


@login_required
def delete_account(request):
  if request.method == 'POST':
    user = request.user
    user.delete()
    logout(request)
    return redirect('/')