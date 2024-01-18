from django.urls import path
from . import views

urlpatterns = [
 
 #users profile view....
    path('admin_profile/<int:admin_id>/', views.admin_profile, name='admin_profile'),
    path('student_acprofile/<int:student_id>/', views.student_acprofile, name='student_acprofile'),
    path('teacher_acprofile/<int:teacher_id>/', views.teacher_acprofile, name='teacher_acprofile'),
    path('parent_acprofile/<int:parent_id>/', views.parent_acprofile, name='parent_acprofile'),
    path('profile/<int:priest_id>/', views.priest_acprofile, name='priest-profile'),




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
    path('addNotice/', views.addNotice,name='addNotice'),
    path('Notice/', views.display_notices,name='display_notices'),
    path('update_notice/<int:notice_id>/', views.update_notice, name='update_notice'),
    path('add_teacher_notice/', views.add_teacher_notice, name='add_teacher_notice'),
    path('display_teacher_notices/', views.display_teacher_notices, name='display_teacher_notices'),
  #preist registeration..
    path('priest-registration', views.register_priest, name='register_priest'),
    path('view_priests/', views.view_priests, name='view_priests'),

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
  path('admin_review_leaves/', views.admin_review_leaves, name='admin_review_leaves'),
  path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
  path('update_marks/<int:student_id>/', views.update_student_marks, name='update_student_marks'),
  path('scheduled-classes/', views.scheduled_classes, name='scheduled_classes'),

     
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
  path('s/add_resource/', views.add_resource, name='add_resource'),
  # path('add_resource/', views.add_resource, name='add_resource'),
  path('index_resource/', views.index_resource, name='index_resource'),

  path('edit_resource/<int:id>/', views.edit_resource, name='edit_resource'),
  path('delete_resource/<int:id>/', views.delete_resource, name='delete_resource'),
  path('class_students', views.class_student, name='class_student'),
  path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
  path('admin_view_attendance/', views.admin_view_attendance, name='attendance'),
  path('teacher/review_leave/', views.teacher_review_leave_applications, name='teacher_review_leave_applications'),
  path('approved_leave/', views.student_leave_approve, name='student_leave_approve'),
  path('staff/leave/apply/', views.staff_leave_apply, name='staff_leave_apply'),
  path('view_class_attendance/', views.view_class_attendance, name='view_class_attendance'),
  path('schedule_class/', views.schedule_class, name='schedule_class'),
 #student dashboard
  path('d/<int:id>/',views.downloadresource,name='downloadresource'),
  path('student_resources/',views.student_resources,name='student_resource'),
  path('online-classes/', views.online_classes, name='online-classes'),
 path('attend-class/<int:class_id>/', views.attend_class, name='attend-class'),

  
  path('student_leave/',views.student_leave_view,name='student_leave_view'),
  path('view_attendance/', views.view_student_attendance, name='view_student_attendance'),

 #parent dashaboard...
  path('parent/',views.parentdashboard,name='parentdashboard'),
  path('view_attendance/', views.view_student_attendance, name='view_attendance'),
  path('download_resource/<int:resource_id>/', views.download_resource, name='download_resource'),
  path('view_resources/', views.view_resources, name='view_resources'),

  #priest dashboard...
  path('priest/',views.priestdashboard,name='priestdashboard'),

  
]