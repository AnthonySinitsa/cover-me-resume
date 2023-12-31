import os
import json
import openai
import requests
import logging
import pdfkit
import asyncio
from io import BytesIO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import UserRegisterForm, ResumeUploadForm, EditCoverLetterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Resume, CoverLetter, Job
from django.http import JsonResponse, FileResponse, HttpResponse
from django.conf import settings
from .utils.pdf_utils import extract_text_from_pdf
from .utils.text_utils import strip_html_tags
from wsgiref.util import FileWrapper
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
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
def home(request):
  context = {}
  job_searched = False
  
  if request.method == 'POST':
    # Resume Upload
    resume_form = ResumeUploadForm(request.POST, request.FILES)
    if resume_form.is_valid():
      # Always get the existing resume or create a new one if it doesn’t exist
      existing_resume, created = Resume.objects.get_or_create(user=request.user)
      
      # Update the resume file with the new one
      existing_resume.resume_file = resume_form.cleaned_data['resume_file']
      try:
        existing_resume.save()
        print("Resume successfully uploaded.")
      except ValidationError as e:
        print(f"Error uploading resume: {e}")
        context['upload_error'] = "Failed to upload resume. Please try again."
      else:
        if not created:
          print("Old resume file overwritten.")

    # Job Search
    job_title = request.POST.get('job_title')
    job_location = request.POST.get('location')
    if job_title and job_location:      
      # Send the scraping task to Celery
      task = run_scraper.delay(job_title, job_location, request.user.id)

      # Save task ID in the session
      request.session['task_id'] = str(task.id)
      request.session.save()

      # Set a flag to indicate a job search was initiated
      job_searched = True
      context['task_id'] = task.id
  
  # If job search was initiated, render the loading page, else render home page
  if job_searched:
    return render(request, 'loading.html', context)
  else:
    context['resume_form'] = ResumeUploadForm()
    return render(request, 'home.html', context)


@login_required
def profile(request):
  resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
  cover_letters = CoverLetter.objects.filter(user=request.user).order_by('-generated_at')
  # Filter out resumes that do not have a file associated with them
  resumes = [resume for resume in resumes if resume.resume_file]
  return render(request, 'profile.html', {'resumes': resumes, 'cover_letters': cover_letters})

@login_required
def job_results(request, task_id=None):
  if task_id:
    # Save task ID in user's session
    request.session['job_results_uuid'] = task_id
    
    # Get the logged-in user's ID
    user_id = request.user.id

    # Step 1: Query the database to get the job data associated with the user
    jobs = Job.objects.filter(user_id=user_id).order_by('post_date')[:30]
    logging.info(f'Job results from views.py: {len(jobs)}')
    
    
    # Step 2: Extracting the Relevant Data
    jobs_list = []
    for job in jobs:
      job_info = {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "post_date": job.post_date,
        "company_overview_link": job.company_overview_link
      }
      jobs_list.append(job_info)

    # Step 3: Passing the Data to the Template
    return render(request, 'job_results.html', {'jobs': jobs_list, 'task_id': task_id})

  messages.error(request, 'No task ID provided.')
  return render(request, 'error_page.html', {'message': 'No task ID provided.'})


@login_required
def generate_cover_letter(request, job_index):
  # Ensure the user has uploaded a resume before proceeding
  user_resume = Resume.objects.filter(user=request.user).first()
  if user_resume is None or not user_resume.resume_file:
    messages.error(request, "You need to upload a resume first.")
    return redirect('home')
  
  # Get the jobs from the database associated with the user
  jobs = list(Job.objects.filter(user=request.user))
  
  # Ensure the job_index is valid
  if job_index < 0 or job_index >= len(jobs):
    messages.error(request, "Invalid job selection.")
    return redirect('home')
  
  # Get the selected job using the job_index
  selected_job = jobs[job_index]
  job_description = selected_job.description

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
  
  # print('sending request to OpenAI API...')
  
  response = requests.post("https://api.openai.com/v1/engines/text-davinci-002/completions", headers=headers, data=json.dumps(data))

  # print("Response received. Status code:", response.status_code)

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
    print('Error:', error_message)
    return render(request, 'error_page.html', {'error_message': error_message})

  cover_letter = response_data['choices'][0]['text'].strip()
  cleaned_cover_letter = strip_html_tags(cover_letter) # THIS ISN'T BEING USED, BUT MAYBE NEED FOR LATER

  # print('generated cover letter:', cover_letter)
  
  # Render the cover letter on a new page or however you wish to display it.
  return render(request, 'cover_letter_page.html', {'cover_letter': cover_letter})

logger = logging.getLogger(__name__)

@login_required
def download_cover_letter(request, cover_letter_id=None):
  try:
    # If cover_letter_id is provided, it means we are serving an already-saved PDF
    if cover_letter_id:
      cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id)
      pdf = cover_letter.pdf_file.read()

      # Extract the custom filename from the stored file name
      custom_filename = cover_letter.pdf_file.name.split("/")[-1].rsplit("_", 1)[0]
      # custom_filename = cover_letter.title

      # Serve the PDF as a response
      response = HttpResponse(pdf, content_type='application/pdf')
      response['Content-Disposition'] = f'attachment; filename="{custom_filename}.pdf"'
      return response

    # If cover_letter_id is not provided, we generate the PDF on-the-fly
    cover_letter_text = request.POST.get('cover_letter_text')

    # Retrieve the custom filename from POST data
    custom_filename = request.POST.get('cover_letter_filename', 'Cover_Letter')

    # Convert newline characters to <br> for proper HTML rendering
    cover_letter_html = cover_letter_text.replace('\n', '<br>')

    # Add the configuration for wkhtmltopdf here
    path_wkhtmltopdf = os.environ.get('WKHTMLTOPDF_PATH', '/app/bin/wkhtmltopdf')
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Convert the HTML to PDF
    pdf = pdfkit.from_string(cover_letter_html, False, configuration=config)

    # Save the generated PDF to the database with the custom filename
    cover_letter_record = CoverLetter(
      user=request.user, 
      content=cover_letter_text,  # <-- This line saves the text content
      pdf_file=ContentFile(pdf, name=f"{custom_filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
    )

    cover_letter_record.save()

    # Serve the generated PDF as a response using the custom filename
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{custom_filename}.pdf"'
    return response
  except Exception as e:
    logger.exception('An error accurred while generating the PDF: %s', e)
    raise e


@login_required
def delete_cover_letter(request, letter_id):
  cover_letter = get_object_or_404(CoverLetter, id=letter_id, user=request.user)
  
  # Delete the file from GCS
  cover_letter.pdf_file.delete(save=False)  # The save=False prevents saving the model after file deletion
  
  # Delete the cover letter record from the database
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
    request.user.delete()
    logout(request)
    return JsonResponse({'status': 'success'})
  return JsonResponse({'status': 'error'}, status=400)
  

@login_required
def edit_cover_letter(request, letter_id):
  cover_letter = get_object_or_404(CoverLetter, id=letter_id, user=request.user)
  filename = cover_letter.pdf_file.name.split("/")[-1].rsplit("_", 1)[0]

  if request.method == 'POST':
    form = EditCoverLetterForm(request.POST, instance=cover_letter)
    if form.is_valid():
      # Get updated text content from the form
      updated_content = form.cleaned_data['content']

      # Convert updated content to HTML for PDF generation
      updated_content_html = updated_content.replace('\n', '<br>')

      # Generate new PDF with updated content
      path_wkhtmltopdf = os.environ.get('WKHTMLTOPDF_PATH', '/app/bin/wkhtmltopdf')
      config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
      updated_pdf = pdfkit.from_string(updated_content_html, False, configuration=config)

      user_provided_title = request.POST.get('cover_letter_filename')

      # Check if the user provided a title; if not, use a default
      custom_filename = user_provided_title if user_provided_title else "Cover_Letter"

      cover_letter.pdf_file.save(
        f"{custom_filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
        ContentFile(updated_pdf)
      )
      
      form.save()
      # Redirect to profile or another page after successful edit
      return redirect('profile')
  else:
    form = EditCoverLetterForm(instance=cover_letter)
    
  context = {'form': form, 'title': filename}
  return render(request, 'edit_cover_letter.html', context)
