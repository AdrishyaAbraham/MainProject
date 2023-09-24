from django.urls import path
from . import views

urlpatterns = [
 
  #hod ...dashboard...student path..

    path('class-wise-student-registration', views.class_wise_student_registration, name='class-wise-student-registration'),
    path('student-registration', views.student_registration, name='student-registration'),
    path('student-list', views.student_list, name='student-list'),
    path('admin_profile/<int:admin_id>/', views.admin_profile, name='admin_profile'),
    path('profile/<reg_no>', views.student_profile, name='student-profile'),
    path('edit/<reg_no>', views.student_edit, name='student-edit'),
    path('delete/<reg_no>', views.student_delete, name='student-delete'),
    path('student-search/', views.student_search, name='student-search'),
    path('enrolled/', views.enrolled_student, name='enrolled-student'),
    path('enrolled-student/<reg>', views.student_enrolled, name='enrolled'),
    path('enrolled-student-list/', views.enrolled_student_list, name='enrolled-student-list'),
    #  path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
   
  #hod---class allotment---
  path('create-class', views.add_class, name='add_class'),
  path('update_class/<int:class_id>/', views.update_class, name='update_class'),
  path('delete_class/<int:class_id>/', views.delete_class, name='delete_class'),
  #class section----------
  path('create-section', views.create_section, name='create-section'),
  path('update-section/<int:section_id>/', views.update_section, name='update_section'),
  path('delete-section/<int:section_id>/', views.delete_section, name='delete_section'),
  #teacher allotment-------
  path('guide-teacher', views.create_guide_teacher, name='guide-teacher'),
  path('registration', views.teacher_registration, name='teacher-registration'),
  path('list', views.teacher_list, name='teacher-list'),
  path('teacher_profile/<teacher_id>', views.teacher_profile, name='teacher_profile'),
  path('teacher_delete/<teacher_id>', views.teacher_delete, name='teacher_delete'),
  path('teacher_edit/<teacher_id>', views.teacher_edit, name='teacher_edit'),
  path('designation', views.add_designation, name='designation'),
  path('designation/<int:designation_id>/', views.update_designation, name='update_designation'),

     
  #class session------------
  path('create-session', views.create_session, name='create-session'),
  path('delete-session/<int:session_id>/', views.delete_session, name='delete-session'),
  path('update-session/<int:session_id>/', views.update_session, name='update-session'),

  #register class--------
  path('class_registration', views.class_registration, name='class-registration'),
  path('class-list', views.class_list, name='class-list'),


  #teacher...dashboard.....
  path('', views.uploadresource, name='uploadresource'),
  path('<int:id>', views.view_resource, name='view_resource'),
  path('add_resource/', views.add_resource, name='add_resource'),
  path('edit_resource/<int:id>/', views.edit_resource, name='edit_resource'),
  path('delete_resource/<int:id>/', views.delete_resource, name='delete_resource'),
 
 #student dashboard
  path('d/<int:id>/',views.downloadresource,name='downloadresource')
  
]