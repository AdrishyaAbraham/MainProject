from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from school.models import *
from school.forms import *


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, TeacherPersonalInfo, ProgressReportRequest
from .forms import ProgressReportRequestForm
from datetime import date

def progress_report(request, reg):
    # Retrieve student information
    student = get_object_or_404(EnrolledStudent, id=reg)
    academic_info = student.student
    personal_info = academic_info.personal_info
    class_name = student.class_name
    
    
    class_info = ClassInfo.objects.get(name=class_name)
    
    # Filter attendance records based on class_info
    attendance_records = Attendance.objects.filter(class_info=class_info)
    academic_year =Session.objects.all()

    # Calculate overall grade and performance summary
    overall_grade = "A"  # Placeholder, calculate based on subject grades
    performance_summary = "Good performance overall."
    subject_name ="Annual Test"
    # Fetch other relevant details
    remarks = "Excellent progress shown."
    recommendations = "Continue with the good work."
    behavior = "Good"
    punctuality = "Excellent"
    cooperation = "Satisfactory"
    behavior_recommendations = "Continue to maintain good behavior."
    teacher_comments = "The student has shown remarkable improvement in academics."
    parent_feedback = "We are pleased with the student's progress."
    school_name = "St.George MTC Sunday School"
    contact_information = "123-456-7890"
    additional_information = "No additional information."
    date_of_issue = date.today() # Set the date of issue

    context = {
        'student': student,
        'academic_info': academic_info,
        'class_info':class_info,
        'personal_info': personal_info,
        'class_name': class_name,
        'academic_year':academic_year,
        'attendance_records': attendance_records,
        'overall_grade': overall_grade,
        'subject_name':subject_name,
        'performance_summary': performance_summary,
        'remarks': remarks,
        'recommendations': recommendations,
        'behavior': behavior,
        'punctuality': punctuality,
        'cooperation': cooperation,
        'behavior_recommendations': behavior_recommendations,
        'teacher_comments': teacher_comments,
        'parent_feedback': parent_feedback,
        'school_name': school_name,
        'contact_information': contact_information,
        'additional_information': additional_information,
        'date_of_issue': date_of_issue,
    }

    return render(request, 'progressreport/progressreport.html', context)

@login_required
def request_progress_report(request, teacher_id):
    # Retrieve the teacher based on the provided ID
    try:
        teacher = TeacherPersonalInfo.objects.get(id=teacher_id)
    except TeacherPersonalInfo.DoesNotExist:
        messages.error(request, "Teacher not found.")
        return redirect('home')  # Redirect to home page or any appropriate URL

    if request.method == 'POST':
        form = ProgressReportRequestForm(request.POST)
        if form.is_valid():
            # Create a progress report request object
            progress_request = form.save(commit=False)
            progress_request.parent = request.user.personal_info  # Assuming parent is logged in
            progress_request.teacher = teacher
            progress_request.save()
            messages.success(request, "Progress report request sent successfully.")
            return redirect('home')  # Redirect to home page or any appropriate URL
    else:
        form = ProgressReportRequestForm()

    return render(request, 'request_progress_report.html', {'form': form, 'teacher': teacher})

@login_required
def student_list(request):
    # Assuming user is logged in and is a GuideTeacher
    try:
        guide_teacher = GuideTeacher.objects.get(name=request.user.teacherpersonalinfo)
    except GuideTeacher.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not a guide teacher!'})

    class_registrations = ClassRegistration.objects.filter(guide_teacher=guide_teacher)
    students = EnrolledStudent.objects.filter(class_name__in=class_registrations)

    # Extract academic_info_id for each student
    academic_info_ids = [student.student.id for student in students]

    context = {
        'students': students,
        'academic_info_ids': academic_info_ids,  # Pass academic_info_ids to the template
    }
    return render(request, 'progressreport/student_list.html', context)
