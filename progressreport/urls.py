from django.urls import path
from .views import *

urlpatterns = [
    path('progress-report/<reg>/', progress_report, name='progress_report'),
    path('class-student/', student_list, name='student-list'),

    # Add more URL patterns as needed
]
