
from django.urls import path
from . import views

urlpatterns = [

path('video_chat/', views.video_chat, name='video_chat'),
path('call/', views.call, name='call'),


]