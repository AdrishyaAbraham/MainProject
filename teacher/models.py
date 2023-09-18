from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
from django.db import models


class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class EducationInfo(models.Model):
    name_of_exam = models.CharField(max_length=100)
    grade = models.CharField(max_length=45)
    passing_year = models.IntegerField()

    def __str__(self):
        return self.name_of_exam

class TrainingInfo(models.Model):
    training_name = models.CharField(max_length=100)
    year = models.IntegerField()
    duration = models.IntegerField()
    place = models.CharField(max_length=100)

    def __str__(self):
        return self.training_name


class ExperienceInfo(models.Model):
    institute_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=45)
    trainer = models.CharField(max_length=45)

    def __str__(self):
        return self.institute_name

class PersonalInfo(models.Model):
    name = models.CharField(max_length=45)
    photo = models.ImageField()
    date_of_birth=models.DateField(null=True)
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
    blood_group_choice = (
        ('a+', 'A+'),
        ('o+', 'O+'),
        ('b+', 'B+'),
        ('ab+', 'AB+'),
        ('a-', 'A-'),
        ('o-', 'O-'),
        ('b-', 'B-'),
        ('ab-', 'AB-')
    )
    blood_group = models.CharField(choices=blood_group_choice, max_length=5)
    phone_regex = RegexValidator(
    regex=r'^(?:\+91-?)?\d{10}$',
    message=(
        "Indian phone number must be entered in the format: '9999999999' or '+91-9999999999'."
        " 10 digits allowed."
    )
)
    phone_no = models.CharField(validators=[phone_regex], max_length=10, blank=True,unique=True)
    email = models.CharField(max_length=30, unique=True)
    address=models.CharField(max_length=255,null=True)
    education = models.ForeignKey(EducationInfo, on_delete=models.CASCADE, null=True)
    training = models.ForeignKey(TrainingInfo, on_delete=models.CASCADE, null=True)
    experience = models.ForeignKey(ExperienceInfo, on_delete=models.CASCADE, null=True)
    is_delete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name