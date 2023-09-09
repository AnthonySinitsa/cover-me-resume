from django.urls import path
from . import views

urlpatterns = [
  path('upload-resume/', views.upload_resume, name='upload-resume'),
  path('profile/', views.profile, name='profile'),
  path('job-search/', views.job_search, name='job_search'),
  path('job-results/', views.job_results, name='job_results'),
  path('generate_cover_letter/<int:job_index>/', views.generate_cover_letter, name='generate_cover_letter'),
  path('download_cover_letter/', views.download_cover_letter, name='download_cover_letter'),
]