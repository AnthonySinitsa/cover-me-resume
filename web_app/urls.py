from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('profile/', views.profile, name='profile'),
  path('job-results/<str:task_id>/', views.job_results, name='job_results'),
  path('generate_cover_letter/<int:job_index>/', views.generate_cover_letter, name='generate_cover_letter'),
  path('download_cover_letter/', views.download_cover_letter, name='download_cover_letter'),
  path('download_cover_letter/<int:cover_letter_id>/', views.download_cover_letter, name='download_cover_letter_by_id'),
  path('delete_cover_letter/<int:letter_id>/', views.delete_cover_letter, name='delete_cover_letter'),
  path('task_status/<str:task_id>/', views.check_task_status, name='check_task_status'),
  path('delete_account/', views.delete_account, name='delete_account'),
  path('edit_cover_letter/<int:letter_id>/', views.edit_cover_letter, name='edit_cover_letter'),
  path('job-results/<str:task_id>/', views.job_results, name='job_results'),
]
