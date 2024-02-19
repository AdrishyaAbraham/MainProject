from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from . models import *
from .models import *
from school.models import *
from django.contrib.auth.decorators import login_required


def online_exam(request):
    if request.method == 'POST':
        # Get the exam schedule ID from the form submission
        exam_schedule_id = request.POST.get('exam_schedule')
        if exam_schedule_id:
            # Retrieve the exam schedule object
            exam_schedule = ExamSchedule.objects.get(id=exam_schedule_id)
            
            # Get the total number of questions from the form
            question_count = int(request.POST.get('question_count'))

            # Iterate through each question
            for i in range(1, question_count + 1):
                # Construct the keys for question text and answer from the form data
                question_text_key = f'question{i}'
                answer_key = f'question{i}_answer'
                
                # Get the question text and correct answer from the form data
                question_text = request.POST.get(question_text_key)
                correct_answer = int(request.POST.get(answer_key))

                # Create the question object and associate it with the exam schedule
                question = Question.objects.create(
                    exam_schedule=exam_schedule,
                    question_text=question_text
                )

                # Iterate through each option for the current question
                for j in range(1, 5):
                    # Construct the key for option text from the form data
                    option_text_key = f'question{i}_option{j}'
                    
                    # Get the option text from the form data
                    option_text = request.POST.get(option_text_key)
                    
                    # Determine if the current option is the correct answer
                    is_correct = (j == correct_answer)

                    # Create the option object and associate it with the current question
                    Option.objects.create(
                        question=question,
                        option_text=option_text,
                        is_correct=is_correct
                    )

            # Redirect to a success page or another view
            return redirect('success_page')
        else:
            # Return a bad request response if no exam schedule ID is provided
            return HttpResponseBadRequest("Please select an exam schedule.")
    else:
        # Handle GET request or other methods if needed
        return HttpResponse("This view only supports POST requests.")
    
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
        exam_schedules = ExamSchedule.objects.all()
        class_list = ClassInfo.objects.all()
        context = {
            'class_list': class_list,
             'exam_schedules': exam_schedules,
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

def list_questions_and_answers(request, exam_schedule_id):
    exam_schedule = get_object_or_404(ExamSchedule, id=exam_schedule_id)
    questions = exam_schedule.question_set.all()  # Assuming a reverse relation from ExamSchedule to Question model
    context = {
        'exam_schedule': exam_schedule,
        'questions': questions,
    }
    return render(request, 'teacher/onlineexam/list_questions_and_answers.html', context)