from django.urls import path
from . import views


urlpatterns = [
    path('upload_to_drive/', views.upload_file_to_drive, name='upload_to_drive'),
]

