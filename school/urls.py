from django.urls import path
from . import views

urlpatterns = [
 
  #hod ...dashboard...student path..

    path('class-wise-student-registration', views.class_wise_student_registration, name='class-wise-student-registration'),
    path('student-registration', views.student_registration, name='student-registration'),
    path('student-list', views.student_list, name='student-list'),
    path('profile/<reg_no>', views.student_profile, name='student-profile'),
    path('edit/<reg_no>', views.student_edit, name='student-edit'),
    path('delete/<reg_no>', views.student_delete, name='student-delete'),
    path('student-search/', views.student_search, name='student-search'),
    path('enrolled/', views.enrolled_student, name='enrolled-student'),
    path('enrolled-student/<reg>', views.student_enrolled, name='enrolled'),
    path('enrolled-student-list/', views.enrolled_student_list, name='enrolled-student-list'),
  
  #hod---class allotment---
  path('create-class', views.add_class, name='add_class'),
  #class section----------
  path('create-section', views.create_section, name='create-section'),
  path('update-section/<int:section_id>/', views.update_section, name='update_section'),
  path('delete-section/<int:section_id>/', views.delete_section, name='delete_section'),
  #teacher allotment-------
  path('guide-teacher', views.create_guide_teacher, name='guide-teacher'),
  #class session------------
  path('create-session', views.create_session, name='create-session'),
  path('delete-session/<int:session_id>/', views.delete_session, name='delete-session'),
  path('update-session/<int:session_id>/', views.update_session, name='update-session'),

  #register class--------
  path('class_registration', views.class_registration, name='class-registration'),
  path('class-list', views.class_list, name='class-list'),


  #teacher...dashboard.....
  path('', views.uploadresource, name='uploadresource'),
  path('r/',views.index_resource, name='index_resource'),
  path('<int:id>', views.view_resource, name='view_resource'),
  path('add_resource/', views.add_resource, name='add_resource'),
  path('edit_resource/<int:id>/', views.edit_resource, name='edit_resource'),
  path('delete_resource/<int:id>/', views.delete_resource, name='delete_resource'),
 
 #student dashboard
  path('d/<int:id>/',views.downloadresource,name='downloadresource')
  
]