import os
import json
import openai
import requests
import pdfkit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ResumeUploadForm
from django.contrib.auth.decorators import login_required
from .models import Resume
from django.http import JsonResponse, FileResponse, HttpResponse
from django.conf import settings
from .utils.pdf_utils import extract_text_from_pdf
from .utils.text_utils import strip_html_tags
from wsgiref.util import FileWrapper


class HomePageView(LoginRequiredMixin, TemplateView):
  template_name = 'home.html'


def register(request):
  """Handle user registration.

    This view function handles user registration requests. It supports both GET and POST requests.
    When a GET request is received, it displays a registration form.
    When a POST request is received with valid form data, it creates a new user account and redirects to the login page.
    
    Parameters:
    - request (HttpRequest): The HTTP request object containing user data and method.

    Returns:
    - HttpResponse: A response containing the registration form or a redirect to the login page.

    Example usage:
    To register a user, make a POST request with valid user registration data.
    To display the registration form, make a GET request to this view.

    Note:
    This view expects a 'UserRegisterForm' instance to be available for user registration.
    The 'registration/register.html' template is used to render the registration form."""
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
  """View for uploading a user's resume.

This view requires authentication, and users must be logged in to access it.

When accessed via POST request, it validates and saves the uploaded resume file
associated with the logged-in user. If the form is valid, it associates the resume
with the user and redirects to the 'home' page or another specified destination upon
successful upload.

Parameters:
    request (HttpRequest): The HTTP request object containing user data.

Returns:
    HttpResponse: A rendered HTML page with an upload form if accessed via GET request,
    or a redirection to the 'home' page (or another specified destination) upon
    successful resume upload via POST request.

Note:
    The 'upload_resume.html' template should be used for rendering the upload form.
    To customize the redirection destination, change the 'return redirect('home')'
    line to the desired URL."""
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
  """View function for displaying a user's profile page, which includes a list of their resumes.

    This view retrieves all the resumes associated with the authenticated user and renders
    them on the 'profile.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered HTML response displaying the user's profile and their resumes.

    Raises:
        None

    Required Permissions:
        - User must be authenticated (@login_required decorator).

    Template:
        - 'profile.html': This template is used to render the user's profile page.

    Context:
        - 'resumes' (QuerySet): A QuerySet containing the user's resumes.

    Usage:
        This view is typically accessed by authenticated users to view their profile page,
        which includes a list of their resumes."""
  user_resumes = Resume.objects.filter(user=request.user)
  context = {'resumes': user_resumes}
  return render(request, 'profile.html', context)


def job_search(request):
  """Handle job search form submission.

    This view function is responsible for processing job search form submissions.
    When a POST request is received, it extracts the job title and job location
    from the form data, then initiates a job scraping process using an external
    scraper module (indeed_scraper). After scraping, it redirects the user to
    the job results page. When the request method is not POST, it renders the
    initial job search form.

    Args:
        request (HttpRequest): The HTTP request object containing form data.

    Returns:
        HttpResponse: Redirects to 'job_results' page after scraping (POST request),
        or renders 'job_search.html' with the initial search form (GET request)."""
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
  """Retrieves job data from a JSON file, extracts relevant information, and renders it in a template.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: A rendered HTML page displaying job results.
    
    This function performs the following steps:
    1. Reads job data from the 'web_app/scrapers/indeed_scraper/results/jobs.json' file.
    2. Extracts relevant job information, including job description, company name, and company overview link.
    3. Passes the extracted data to the 'job_results.html' template for rendering.

    Example Usage:
    To display job results, call this function with an appropriate HTTP request object."""
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
  """Extracts text content from a PDF resume file and returns it as plain text.

    Parameters:
    resume_file_path (str): The file path to the PDF resume to be processed.

    Returns:
    str: The extracted text content from the PDF resume.

    Raises:
    FileNotFoundError: If the specified resume_file_path does not exist.
    ValueError: If the file at resume_file_path is not a valid PDF.

    Example:
    >>> text = get_user_resume_as_text("path/to/resume.pdf")
    >>> print(text)
    "John Doe\n123 Main Street\nCity, State ZIP\nPhone: (123) 456-7890\nEmail: johndoe@email.com\n..."

    This function takes a PDF resume file and uses the 'extract_text_from_pdf' function to
    extract its textual content. It is designed to handle exceptions for missing files
    and invalid PDFs, raising appropriate errors. The extracted text is returned as a string."""
  return extract_text_from_pdf(resume_file_path)

@login_required
def generate_cover_letter(request, job_index):
  """ Generate a cover letter for a job application.

    This function takes the user's request and a job index as input. It retrieves the job description
    from a JSON file, the user's resume, and then uses the OpenAI API to generate a cover letter
    based on the provided job description and the user's resume.

    Args:
        request (HttpRequest): The HTTP request object from Django.
        job_index (int): The index of the job for which to generate the cover letter.

    Returns:
        HttpResponse: A response containing the generated cover letter or an error message page.

    Raises:
        ValueError: If there is no resume found for the user.

    Note:
        The generated cover letter is displayed to the user on a separate page."""
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
  openai_api_key = settings.OPENAI_API_KEY
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
def download_cover_letter(request):
    # This example assumes that you are posting the cover letter text from a form.
    # You can adjust this as necessary.
    cover_letter_text = request.POST.get('cover_letter_text')

    # Convert newline characters to <br> for proper HTML rendering
    cover_letter_html = cover_letter_text.replace('\n', '<br>')

    # Convert the HTML to PDF
    pdf = pdfkit.from_string(cover_letter_html, False)

    # Serve the PDF as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cover_letter.pdf"'
    return response
