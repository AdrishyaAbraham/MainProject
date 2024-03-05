from django.db import models
from django.core.validators import RegexValidator
import random
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from django.db.models import Avg
from django.core.validators import RegexValidator
# Create your models here.
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db import models
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, mobile=None, address=None,role=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile=mobile, address=address, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, role=None, mobile=None):
        role='admin'
        user = self.create_user(email=email, name=name, password=password, role=role, mobile=mobile)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    USER_ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
        ('priest', 'Priest'),
        ('parent', 'Parent'),

    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=15, choices=USER_ROLES, blank=True, null=True,default='student')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    
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
    training_name = models.CharField(max_length=50)
    year = models.IntegerField()
    duration = models.IntegerField()
    place = models.CharField(max_length=50)

    def __str__(self):
        return self.training_name


class ExperienceInfo(models.Model):
    institute_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=45)
    trainer = models.CharField(max_length=45)

    def __str__(self):
        return self.institute_name
    


#Attendance................#
class PreistPersonalInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,blank=True,null=True)
    emergency_contact_phone = models.CharField(max_length=15)
    ordination_date = models.DateField()
    diocese = models.CharField(max_length=255)
    previous_parish = models.TextField(blank=True, null=True)
    availability = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.name}"
    
class TeacherPersonalInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,blank=True,null=True)
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
    education = models.ForeignKey(EducationInfo, on_delete=models.CASCADE, null=True)
    training = models.ForeignKey(TrainingInfo, on_delete=models.CASCADE, null=True)
    experience = models.ForeignKey(ExperienceInfo, on_delete=models.CASCADE, null=True)
    is_delete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.name
  



class Section(models.Model):
    name = models.CharField(max_length=45, unique=True)
    date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False) 
    def __str__(self):
        return self.name

class GuideTeacher(models.Model):
    name = models.OneToOneField(TeacherPersonalInfo, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False) 
    def __str__(self):
        return str(self.name)
    
class Session(models.Model):
    name = models.CharField(unique=True, max_length=4)  # Assuming the year is a 4-digit number
    date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    
class ClassInfo(models.Model):
    name = models.CharField(max_length=45, unique=True)
    display_name = models.CharField(max_length=10, unique=True)
    date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return self.display_name
        
class ClassRegistration(models.Model):
    name = models.CharField(max_length=15, unique=True)
    class_name = models.ForeignKey(ClassInfo, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    guide_teacher = models.OneToOneField(GuideTeacher, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['class_name', 'section', 'guide_teacher']

    def __str__(self):
        return self.name
    

class Resource(models.Model):
    resource_id=models.PositiveBigIntegerField()
    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE,null=True)
    teacher_name= models.ForeignKey(TeacherPersonalInfo, on_delete=models.CASCADE, null=True)
    class_registration = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE,null=True)
    resource_title=models.CharField(max_length=60,null=True)
    resource_file=models.FileField(upload_to='notes/pdfs/',null=True)
    file_type=models.CharField(max_length=30,null=True)
    description=models.CharField(max_length=200,null=True)
    uploaded_date = models.DateField(auto_now_add=True,null=True)
    def __str__(self) -> str:
        return f'Resourse: {self.resource_title}'

class GuardianInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    father_name = models.CharField(max_length=100)
    father_phone_no = models.CharField(max_length=10,unique=True)
    mother_name = models.CharField(max_length=100)
    mother_phone_no = models.CharField(max_length=10,unique=True)
    guardian_name = models.CharField(max_length=100)
    guardian_phone_no = models.CharField(max_length=10)
    guardian_email = models.EmailField(blank=True, null=True)
    relationship_choice = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
    )
    relationship_with_student = models.CharField(choices=relationship_choice, max_length=45)

    def __str__(self):
        return self.father_name



class PersonalInfo(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    guardian = models.ForeignKey(GuardianInfo, on_delete=models.CASCADE,null=True)
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
    date_of_birth = models.DateField()
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
    phone_regex = RegexValidator(
    regex=r'^(?:\+91-?)?\d{10}$',
    message=(
        "Indian phone number must be entered in the format: '9999999999' or '+91-9999999999'."
        " 10 digits allowed."
    )
)

    def __str__(self):
        return self.user.name
    
 


class PreviousAcademicInfo(models.Model):
    institute_name = models.CharField(max_length=100)
    name_of_exam = models.CharField(max_length=100)
    board_roll = models.IntegerField()
    passing_year = models.CharField(max_length=4)

    def __str__(self):
        return self.institute_name

class PreviousAcademicCertificate(models.Model):
    marksheet = models.FileField(upload_to='documents/', blank=True)
    other_certificate = models.FileField(upload_to='documents/', blank=True)

class AcademicInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='academic_info',null= True)
    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
    registration_no = models.IntegerField(unique=True, default=random.randint(000000, 999999))
    status_select = (
        ('not enroll', 'Not Enroll'),
        ('enrolled', 'Enrolled'),
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('passed', 'Passed'),
    )
    status = models.CharField(choices=status_select, default='not enroll', max_length=15)
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, null=True)
    guardian_info = models.ForeignKey(GuardianInfo, on_delete=models.CASCADE, null=True)
    previous_academic_info = models.ForeignKey(PreviousAcademicInfo, on_delete=models.CASCADE, null=True)
    previous_academic_certificate = models.ForeignKey(PreviousAcademicCertificate, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class EnrolledStudent(models.Model):
    class_name = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE)
    student = models.OneToOneField(AcademicInfo, on_delete=models.CASCADE)
    roll = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['class_name', 'roll']
    
    def __str__(self):
        return str(self.student)    
        
class Attendance(models.Model):
    class_info = models.ForeignKey(ClassInfo, on_delete=models.DO_NOTHING,null=True)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


 
 
class AttendanceReport(models.Model):
    # Individual Student Attendance
    student_id = models.ForeignKey(PersonalInfo, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class LeaveReportStudent(models.Model):
     PENDING = 0
     APPROVED = 1
     REJECTED = 2

     LEAVE_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
     ]


     leave_status = models.IntegerField(choices=LEAVE_STATUS_CHOICES, default=PENDING)
     student_id = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
     leave_date = models.DateField(null=True)
     leave_message = models.CharField(max_length=255)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     objects = models.Manager()

 
class LeaveReportStaff(models.Model):

    PENDING = 0
    APPROVED = 1
    REJECTED = 2

    LEAVE_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
     ]


    staff_id = models.ForeignKey(TeacherPersonalInfo, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(choices=LEAVE_STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def approve(self):
        self.leave_status = self.APPROVED
        self.save()

    def reject(self):
        self.leave_status = self.REJECTED
        self.save()

class Notice(models.Model):
    title=models.CharField(max_length=50,null=True)
    Message = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Message

class TeacherNotice(models.Model):
    
    title=models.CharField(max_length=50,null=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='teacher_notices')
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return self.message


# models.py
class Mark(models.Model):
    student = models.ForeignKey(EnrolledStudent, on_delete=models.CASCADE)
    subject1 = models.PositiveIntegerField(null=True, blank=True)
    class_name = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        student_name = self.student.student.personal_info.user.name if self.student.student else "Unknown"
        return f"{student_name} - Marks"


    
class ScheduledClass(models.Model):
    enrolled_class = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE)
    teacher = models.ForeignKey(GuideTeacher, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    platform_link = models.URLField()


class OnlineClass(models.Model):
    teacher = models.ForeignKey(GuideTeacher, on_delete=models.CASCADE,null=True, blank=True)
    class_name = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class TalentProgram(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()


    def __str__(self):
        return self.name
    
class Registration(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    program = models.ForeignKey(TalentProgram, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'program')

    def __str__(self):
        return f"{self.student.username} - {self.program.name}"
    


class CounselingSession(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_sessions', on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teacher_sessions', on_delete=models.CASCADE)
    chat_room_link = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.student.username} - {self.teacher.username} Counseling"
    


class Certificate(models.Model):
    enrolled_student = models.ForeignKey(EnrolledStudent, on_delete=models.CASCADE)
    class_associated = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='certificates/')
    issue_date = models.DateField()
    is_previous_class = models.BooleanField(default=False)

    def __str__(self):
        return f"Certificate for {self.enrolled_student} - {'Previous Class' if self.is_previous_class else 'Current Class'}"



#online exams.........
 
    
class ExamSchedule(models.Model):
    hod = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class_name = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    date = models.DateField()
    start_time = models.TimeField()
    duration_hours = models.IntegerField(default=1)  # Duration in hours
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - Class {self.class_name} - {self.date} -{self.start_time}"