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
        ('Priest', 'Priest'),
        ('Parent', 'Parent'),

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
        return self.email
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
  


class Resource(models.Model):
    resource_id=models.PositiveBigIntegerField()
    teacher_name= models.ForeignKey(TeacherPersonalInfo, on_delete=models.CASCADE, null=True)
    resource_title=models.CharField(max_length=60,null=True)
    resource_file=models.FileField(upload_to='notes/pdfs/',null=True)
    file_type=models.CharField(max_length=30,null=True)
    description=models.CharField(max_length=200,null=True)
    uploaded_date = models.DateField(auto_now_add=True,null=True)
    def __str__(self) -> str:
        return f'Resourse: {self.resource_title}'

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
    name = models.IntegerField(unique=True)
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
    


class PersonalInfo(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
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
    
 

class GuardianInfo(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE,null=True)
    father_name = models.CharField(max_length=100)
    father_phone_no = models.CharField(max_length=10,unique=True)
    mother_name = models.CharField(max_length=100)
    mother_phone_no = models.CharField(max_length=10,unique=True)
    guardian_name = models.CharField(max_length=100)
    guardian_phone_no = models.CharField(max_length=10)
    guardian_email = models.EmailField(blank=True, null=True,unique=True)
    relationship_choice = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
    )
    relationship_with_student = models.CharField(choices=relationship_choice, max_length=45)

    def __str__(self):
        return self.guardian_name



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
        return str(self.registration_no)

class EnrolledStudent(models.Model):
    class_name = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE)
    student = models.OneToOneField(AcademicInfo, on_delete=models.CASCADE)
    roll = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['class_name', 'roll']
    
    def __str__(self):
        return str(self.roll)    
