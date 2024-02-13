from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from . models import *
from .models import *
from school.models import *
from django.contrib.auth.decorators import login_required

def online_exam(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration_hours = request.POST.get('duration_hours')
        class_name_id = request.POST.get('class_name_id')  # Assuming the class_name_id is provided in the form
        
        # Check if all required fields are provided
        if date and start_time and duration_hours and class_name_id:
            # Get the ClassInfo instance
            class_name = ClassInfo.objects.get(id=class_name_id)
            
            # Find an existing ExamSchedule instance for the given date, start time, and class
            exam_schedule = ExamSchedule.objects.filter(date=date, start_time=start_time, class_name=class_name).first()
            
            if not exam_schedule:
                # If an ExamSchedule doesn't exist for the given parameters, handle the situation accordingly
                return HttpResponseBadRequest("No exam schedule found for the given parameters.")
            
            # Get the number of questions dynamically added to the form
            question_count = int(request.POST.get('question_count'))
            
            # Loop through each question and its options
            for i in range(1, question_count + 1):
                question_text = request.POST.get(f'question{i}')
                correct_option_index = int(request.POST.get(f'question{i}_answer'))
                
                # Create the Question instance associated with the retrieved ExamSchedule
                question = Question.objects.create(exam_schedule=exam_schedule, question_text=question_text)
                
                # Loop through each option for the current question
                for j in range(1, 5):  # Assuming there are always 4 options
                    option_text = request.POST.get(f'question{i}_option{j}')
                    
                    # Determine if the current option is correct based on its index
                    is_correct = (j == correct_option_index)
                    
                    # Create the Option instance
                    Option.objects.create(question=question, option_text=option_text, is_correct=is_correct)
            
            # Redirect to a success page or another view
            return redirect('exam_schedule_detail', pk=exam_schedule.pk)
        else:
            # If any required field is missing, return a bad request response
            return HttpResponseBadRequest("Missing required parameters")
    else:
        default_date = '2024-02-09'  # Default date, you can change this
        default_start_time = '09:00'  # Default start time, you can change this
        default_duration_hours = '2'  # Default duration hours, you can change this
        
        context = {
            'default_date': default_date,
            'default_start_time': default_start_time,
            'default_duration_hours': default_duration_hours,
        }
        # Render the form template
        return render(request, 'teacher/onlineexam/set_questions.html', context)



@login_required
def take_exam(request, exam_schedule_id):
    exam_schedule = ExamSchedule.objects.get(pk=exam_schedule_id)
    questions = Question.objects.filter(exam_schedule=exam_schedule)
    
    if request.method == 'POST':
        # Handle form submission
        submission = StudentExamSubmission.objects.create(student=request.user, exam_schedule=exam_schedule)
        
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}_option')
            if selected_option_id:
                selected_option = Option.objects.get(pk=selected_option_id)
                StudentAnswer.objects.create(submission=submission, question=question, selected_option=selected_option)
        
        # Redirect to a submission confirmation page
        return redirect('submission_confirmation')
    
    context = {
        'exam_schedule': exam_schedule,
        'questions': questions,
    }
    return render(request, 'student/take_exam.html', context)

@login_required
def submission_confirmation(request):
    return render(request, 'submission_confirmation.html')


from django.utils import timezone

def schedule_exam(request):
    if request.method == 'POST':
        # Handle form submission to schedule an exam
        hod = request.user  # Assuming the current user is the HOD
        class_name_id = request.POST.get('class_name')
        class_name = ClassInfo.objects.get(id=class_name_id)
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration_hours = request.POST.get('duration_hours')
        
        # Check if there's already an exam scheduled for the selected class on the specified date
        existing_exam = ExamSchedule.objects.filter(class_name=class_name, date=date).exists()
        if existing_exam:
            # If an exam already exists for the same class and date, return an error message
            error_message = 'An exam is already scheduled for the selected class on the specified date.'
            class_list = ClassInfo.objects.all()
            context = {
                'class_list': class_list,
                'error_message': error_message
            }
            return render(request, 'hod/schedule_exam.html', context)
        else:
            # No existing exams found for the same class and date, create the ExamSchedule instance
            exam_schedule = ExamSchedule.objects.create(
                hod=hod,
                class_name=class_name,
                subject=subject,
                date=date,
                start_time=start_time,
                duration_hours=duration_hours
            )
            return redirect('exam_schedule_detail')
    else:
        # Fetch all classes
        class_list = ClassInfo.objects.all()
        context = {
            'class_list': class_list,
             # Default start time, you can change this
        }
        # Render a template with a form to schedule an exam along with the list of classes
        return render(request, 'hod/schedule_exam.html', context)


def exam_schedule_detail(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        selected_class = get_object_or_404(ClassInfo, pk=class_id)
        exam_schedules = ExamSchedule.objects.filter(class_name=selected_class)
    else:
        exam_schedules = ExamSchedule.objects.all()
    
    class_list = ClassInfo.objects.all()
    
    context = {
        'exam_schedules': exam_schedules,
        'class_list': class_list,
    }
    return render(request, 'hod/exam_schedule_detail.html', context)

def submit_exam(request, exam_schedule_pk):
    if request.method == 'POST':
        # Process exam submission
        exam_schedule = ExamSchedule.objects.get(pk=exam_schedule_pk)
        student = request.user
        submission = StudentExamSubmission.objects.create(exam_schedule=exam_schedule, student=student)
        questions = Question.objects.filter(exam_schedule=exam_schedule)
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.pk}_option')
            if selected_option_id:
                selected_option = Option.objects.get(pk=selected_option_id)
                StudentAnswer.objects.create(submission=submission, question=question, selected_option=selected_option)
        return redirect('exam_submission_confirmation')
    else:
        # Render a template with a form to submit an exam (if needed)
        exam_schedule = ExamSchedule.objects.get(pk=exam_schedule_pk)
        questions = Question.objects.filter(exam_schedule=exam_schedule)
        return render(request, 'submit_exam.html', {'exam_schedule': exam_schedule, 'questions': questions})

def exam_submission_confirmation(request):
    return render(request, 'exam_submission_confirmation.html')


# Create your views here.
