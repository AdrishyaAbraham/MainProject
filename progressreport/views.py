from django.shortcuts import render
from school.models import *


def progress_report(request, academic_info_id):
    # Retrieve academic information for the student
    academic_info = AcademicInfo.objects.get(id=academic_info_id)

    # Retrieve marks for the student
    marks = Mark.objects.filter(student__academic_info=academic_info)

    # Retrieve attendance records for the student
    attendance_reports = AttendanceReport.objects.filter(student_id=academic_info.user.personalinfo.id)

    # Additional context data
    overall_grade = "A"  # Calculate overall grade based on subject grades
    performance_summary = "Good performance overall."
    remarks = "Excellent progress shown."
    recommendations = "Continue with the good work."

    behavior = "Good"
    punctuality = "Excellent"
    cooperation = "Satisfactory"
    behavior_recommendations = "Continue to maintain good behavior."

    teacher_comments = "The student has shown remarkable improvement in academics."
    parent_feedback = "We are pleased with the student's progress."

    school_name = "ABC School"
    contact_information = "123-456-7890"
    additional_information = "No additional information."

    date_of_issue = "February 28, 2024"

    context = {
        'student': academic_info.user.personalinfo,
        'marks': marks,
        'attendance_reports': attendance_reports,
        'overall_grade': overall_grade,
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

    return render(request, 'progress_report.html', context)