from django.urls import path
from .views import progress_report_card_view

urlpatterns = [
    path('progress-report/', progress_report_card_view, name='progress_report_card'),
    # Add more URL patterns as needed
]
