from django.db import models
from django.core.validators import RegexValidator
import random
from teacher.models import PersonalInfo
from django.utils import timezone
from django.core.exceptions import ValidationError

class Resource(models.Model):
    resource_id=models.PositiveBigIntegerField()
    teacher_name= models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, null=True)
    resource_title=models.CharField(max_length=60,null=True)
    resource_file=models.FileField(upload_to='notes/pdfs/',null=True)
    file_type=models.CharField(max_length=30,null=True)
    description=models.CharField(max_length=200,null=True)
    uploaded_date = models.DateField(auto_now_add=True,null=True)
    def __str__(self) -> str:
        return f'Resourse: {self.resource_title}'


class Class(models.Model):
    name = models.CharField(max_length=45, unique=True)
    display_name = models.CharField(max_length=10, )
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.display_name

class Section(models.Model):
    name = models.CharField(max_length=45, unique=True)
    date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False) 
    def __str__(self):
        return self.name

class GuideTeacher(models.Model):
    name = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE, null=True)
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
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student-photos/')
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
    phone_no = models.CharField(validators=[phone_regex], max_length=10, blank=True,unique=True)
    email = models.EmailField(blank=True, null=True)
    # password=models.CharField(blank=True,max_length=10)
#     groups = models.ManyToManyField(
#     Group,
#         verbose_name=('groups'),
#         blank=True,
#         help_text=(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#           related_name="student_personalinfo_set",
#     related_query_name="student_personalinfo",
# )
    
    # # Override the user_permissions field
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=('user permissions'),
    #     blank=True,
    #     help_text=('Specific permissions for this user.'),
    #    related_name="student_personalinfo_permissions_set",
    # related_query_name="student_personalinfo_permissions",
    # )
    
   
    # last_login = models.DateTimeField('last login', default=timezone.now)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False) # This is for admin site

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name', 'phone_no']

    def __str__(self):
        return self.name


class GuardianInfo(models.Model):
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

class EmergencyContactDetails(models.Model):
    emergency_guardian_name = models.CharField(max_length=100)
    address = models.TextField()
    relationship_choice = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
    )
    relationship_with_student = models.CharField(choices=relationship_choice, max_length=45)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.emergency_guardian_name

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
    emergency_contact_info = models.ForeignKey(EmergencyContactDetails, on_delete=models.CASCADE, null=True)
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



