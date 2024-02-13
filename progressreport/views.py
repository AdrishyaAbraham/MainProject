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
        'overall_grade': 'A',
        'overall_summary': 'Excellent performance in most subjects',
        'overall_remarks': 'Keep up the good work',
        'overall_recommendations': 'Work on improving performance in History',
        'behavior': 'Excellent',
        'punctuality': 'Always on time',
        'cooperation': 'Very cooperative',
        'behavior_recommendations': 'Continue to maintain good behavior',
        'teacher_comments': 'John has shown great improvement in his problem-solving skills. He should continue practicing regularly to excel further.',
        'parent_feedback': 'Please contact us for any further discussion or clarification regarding John\'s progress.',
        'school_name': 'ABC School',
        'contact_information': '123-456-7890 | info@abcschool.com',
        'principal_signature': '[Signature]',
        'additional_information': 'Special Achievements: John won the first prize in the Science Fair',
        'grading_scale': 'A: 90-100 (Excellent), B: 80-89 (Good), C: 70-79 (Satisfactory), D: 60-69 (Needs Improvement)',
        'date_of_issue': 'February 9, 2024',
    }
    
    return render(request, 'progressreport/progressreport.html', context)
