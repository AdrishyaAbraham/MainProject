from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def progress_report_card_view(request):
    # Context data for the template
    context = {
        'student_name': 'John Doe',
        'student_id': '123456',
        'class_grade': '10th Grade',
        'academic_year': '2023-2024',
        'subjects': [
            {'name': 'Mathematics', 'grade': 'A', 'comments': 'Excellent performance', 'attendance': '90%'},
            # Add more subjects as needed
        ],
    }
    
    return render(request, 'progressreport/progressreport.html', context)
