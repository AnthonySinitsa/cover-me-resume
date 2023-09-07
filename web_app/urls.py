from django.urls import path
from . import views

urlpatterns = [
  path('upload-resume/', views.upload_resume, name='upload-resume'),
  path('profile/', views.profile, name='profile'),
]