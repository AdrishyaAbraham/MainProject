from django.urls import path
from . import views

urlpatterns = [
  path('1/', views.index1, name='index'),
  path('', views.base, name='base'),
  path('<int:id>', views.view_student, name='view_student'),
  path('add/', views.add, name='add'),
  path('edit/<int:id>/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),

  #teacher path...
  path('', views.index2, name='index2'),
  path('', views.base_teacher, name='base_teacher'),
  path('<int:id>', views.view_teacher, name='view_teacher'),
  path('add_teacher/', views.add_teacher, name='add_teacher'),
  path('edit/<int:id>/', views.edit_teacher, name='edit_teacher'),
  path('delete/<int:id>/', views.delete_teacher, name='delete_teacher'),

  #hod dashboard...teacher path...
  path('2/', views.index2, name='index2'),
  path('', views.base_teacher, name='base_teacher'),
  path('<int:id>', views.view_teacher, name='view_teacher'),
  path('add_teacher/', views.add_teacher, name='add_teacher'),
  path('edit_teacher/<int:id>/', views.edit_teacher, name='edit_teacher'),
  path('delete_teacher/<int:id>/', views.delete_teacher, name='delete_teacher'),
 

  #hod ...dashboard...student path..
  path('1/', views.index1, name='index'),
  path('b/', views.base, name='base'),
  path('<int:id>', views.view_student, name='view_student'),
  path('add/', views.add, name='add'),
  path('edit/<int:id>/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),
  path('v/', views.editprofile, name='editprofile'),
  
  #hod---class allotment---
  path('create-class', views.add_class, name='add_class'),
  path('create-section', views.create_section, name='create-section'),
  path('create-section', views.create_section, name='create-section'),
  path('guide-teacher', views.create_guide_teacher, name='guide-teacher'),
  path('create-session', views.create_session, name='create-session'),
  path('class_registration', views.class_registration, name='class-registration'),
  path('class-list', views.class_list, name='class-list'),


  #teacher...dashboard.....
  path('', views.uploadresource, name='uploadresource'),
  path('r/',views.index_resource, name='index_resource'),
  path('<int:id>', views.view_resource, name='view_resource'),
  path('add_resource/', views.add_resource, name='add_resource'),
  path('edit_resource/<int:id>/', views.edit_resource, name='edit_resource'),
  path('delete_resource/<int:id>/', views.delete_resource, name='delete_resource'),

  
]