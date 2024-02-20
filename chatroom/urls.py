
from django.urls import path
from . import views

urlpatterns = [

path('video_chat/', views.video_chat, name='video_chat'),
path('video_chat_students/', views.video_chat_students, name='video_chat_students'),

path('call/', views.call, name='call'),
path('join-room/', views.join_room, name='join_room'),



]