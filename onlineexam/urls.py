  

from django.urls import path
from . import views

urlpatterns = [
path('s/online_exam/', views.online_exam, name='online_exam'),
path('schedule-exam/', views.schedule_exam, name='schedule_exam'),
path('exam-schedule-detail/', views.exam_schedule_detail, name='exam_schedule_detail'),
path('submission_confirmation/', views.submission_confirmation, name='submission_confirmation'),
path('take_exam/<int:exam_schedule_id>/', views.take_exam, name='take_exam'),

]