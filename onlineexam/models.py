from django.db import models
from school.models import *
# Create your models here.
   


class Question(models.Model):
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class StudentExamSubmission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.exam_schedule.subject} - {self.submission_time}"


class StudentAnswer(models.Model):
    submission = models.ForeignKey(StudentExamSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission.student} - {self.question} - {self.selected_option}"
