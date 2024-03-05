from django.urls import path
from .views import *

urlpatterns = [
    path('progress-report/<int:academic_info_id>/', progress_report, name='progress_report'),
    # Add more URL patterns as needed
]
