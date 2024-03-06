import datetime
from time import strptime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from pandas import Timedelta

from .forms import QuestionForm
from . models import *
from .models import *
from school.models import *
from django.contrib.auth.decorators import login_required


def add_questions(request):
    if request.method == 'POST':
        exam_schedule_id = request.POST.get('exam_schedule')
        exam_schedule = ExamSchedule.objects.get(id=exam_schedule_id)
        question_count = int(request.POST.get('question_count'))

        for i in range(1, question_count + 1):
            question_text = request.POST.get(f'question{i}')
            question = Question.objects.create(exam_schedule=exam_schedule, question_text=question_text)

            for j in range(1, 5):
                option_text = request.POST.get(f'question{i}_option{j}')
                is_correct = (j == int(request.POST.get(f'question{i}_answer')))
                Option.objects.create(question=question, option_text=option_text, is_correct=is_correct)

        return redirect('list_questions_and_answers', exam_schedule_id=exam_schedule_id)
  # Redirect to a success page after saving

    else:
        # Fetch all exam schedules to populate the dropdown
        exam_schedules = ExamSchedule.objects.all()
        return render(request, 'teacher/onlineexam/set_questions.html', {'exam_schedules': exam_schedules})

@login_required
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

            # Redirect to the 'list_questions_and_answers' view with the exam_schedule_id argument
            return redirect('list_questions_and_answers', exam_schedule_id=exam_schedule_id)
        else:
            # Return a bad request response if no exam schedule ID is provided
            return HttpResponseBadRequest("Please select an exam schedule.")
    else:
        # Handle GET request or other methods if needed
        return HttpResponse("This view only supports POST requests.")
    


@login_required
def submission_confirmation(request):
    return render(request, 'submission_confirmation.html')


@login_required
def take_exam(request, exam_schedule_id):
    exam_schedule = ExamSchedule.objects.get(id=exam_schedule_id)
    print("Exam Schedule:", exam_schedule)
    questions = Question.objects.filter(exam_schedule=exam_schedule)

    if request.method == 'POST':
        # Process the submitted exam answers
        submission = StudentExamSubmission.objects.create(
            student=request.user,
            exam_schedule=exam_schedule
        )
        total_marks = 0
        print("Questions :")
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}_option')
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                StudentAnswer.objects.create(
                    submission=submission,
                    question=question,
                    selected_option=selected_option
                )
                if selected_option.is_correct:
                    total_marks += 1  # Increment marks if the selected option is correct

        submission.total_marks = total_marks
        submission.save()

        return redirect('exam_results', submission_id=submission.id) 

    context = {
        'exam_schedule': exam_schedule,
        'questions': questions,
    }
    return render(request, 'student/onlineexam/take_exam.html', context)



@login_required
def exam_results(request, submission_id):
    submission = StudentExamSubmission.objects.get(id=submission_id)
    student_answers = StudentAnswer.objects.filter(submission=submission)

    context = {
        'submission': submission,
        'student_answers': student_answers,
    }
    return render(request, 'student/onlineexam/exam_results.html', context)


from django.utils import timezone


from datetime import timedelta


def schedule_exam(request):
    if request.method == 'POST':
        # Retrieve form data
        class_id = request.POST.get('class_name')
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration_hours = request.POST.get('duration_hours')

        # Create datetime object for start time
        start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")

        # Calculate end time based on start time and duration
        end_datetime = start_datetime + timedelta(hours=int(duration_hours))

        # Create ExamSchedule object
        exam_schedule = ExamSchedule(
            class_id=class_id,
            subject=subject,
            start_time=start_datetime,
            end_time=end_datetime
        )
        exam_schedule.save()

        # Redirect to a success page or any other desired URL
        return redirect('success_page')

    else:
        # If it's a GET request, render the form template
        return render(request, 'hod/schedule_exam.html', {'class_list': ClassInfo.objects.all()})
    
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