from django.test import TestCase
from google.cloud import storage

# for this test you must $ export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
# python web_app/tests.py
def list_blobs(bucket_name):
  """Lists all the blobs in the bucket."""
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)

  blobs = bucket.list_blobs()

  for blob in blobs:
    print(blob.name)

# Replace 'your-bucket-name' with the name of your bucket.
list_blobs('resumes-coverletter')





# @login_required
# def home(request):
#   if request.method == 'POST':
#     form = ResumeUploadForm(request.POST, request.FILES)
#     if form.is_valid():
#       # Check if the user already has a resume
#       existing_resume = Resume.objects.filter(user=request.user).first()
      
#       if existing_resume:
#         # If a resume exists, delete the old file from storage
#         existing_resume.resume_file.delete()
        
#         # Update the resume file with the new one
#         existing_resume.resume_file = form.cleaned_data['resume_file']
#         existing_resume.save()
#       else:
#         # If no resume exists, create a new Resume object
#         resume = form.save(commit=False)
#         resume.user = request.user
#         resume.save()

#       # Do not redirect, as we want to stay on the same page
#       form = ResumeUploadForm()  # Reset the form after successful upload
#   else:
#     form = ResumeUploadForm()

#   context = {
#     'resume_form': form
#   }
#   return render(request, 'home.html', {'form': form})