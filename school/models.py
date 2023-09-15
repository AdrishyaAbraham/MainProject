from django.db import models
from django.core.validators import RegexValidator
import random

class Student(models.Model):
    student_number=models.PositiveBigIntegerField(null=True)
    name=models.CharField(max_length=60)
    email=models.EmailField(max_length=100)
    address = models.CharField(max_length=100, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone number must be entered in the format: '+91'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True) # Validators should be a list
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    dob = models.DateField(max_length=8,null=True)
    doj = models.DateField(max_length=8,null=True)
    fathername=models.CharField(max_length=50,null=True)
    father_contact=models.CharField(validators=[phone_regex], max_length=10, blank=True)
    mothername=models.CharField(max_length=50,null=True)
    mother_contact=models.CharField(validators=[phone_regex], max_length=10, blank=True)

    def __str__(self) -> str:
        return f'Student: {self.name} '


class Teacher(models.Model):
    teacher_number=models.PositiveBigIntegerField()
    name=models.CharField(max_length=60)
    email=models.EmailField(max_length=100)
    address = models.CharField(max_length=100, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,110}$', message="Phone number must be entered in the format: '+91'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True) # Validators should be a list
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    dob = models.DateField(max_length=8,null=True)
    doj = models.DateField(max_length=8,null=True)
    
    def __str__(self) -> str:
        return f'Teacher: {self.name} '    

class Resource(models.Model):
    resource_id=models.PositiveBigIntegerField()
    teacher_name= models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True)
    resource_title=models.CharField(max_length=60,null=True)
    resource_file=models.FileField(upload_to='notes/pdfs/',null=True)
    file_type=models.CharField(max_length=30,null=True)
    description=models.CharField(max_length=200,null=True)
    uploaded_date=models.DateField(max_length=30,null=True)

    def __str__(self) -> str:
        return f'Resourse: {self.resource_title}'


class Class(models.Model):
    name = models.CharField(max_length=45, unique=True)
    display_name = models.CharField(max_length=10, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.display_name

class Section(models.Model):
    name = models.CharField(max_length=45, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class GuideTeacher(models.Model):
    name = models.OneToOneField('Teacher', on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
    
class Session(models.Model):
    name = models.IntegerField(unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
    
class ClassRegistration(models.Model):
    name = models.CharField(max_length=10, unique=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    guide_teacher = models.OneToOneField(GuideTeacher, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['class_name', 'section', 'guide_teacher']

    def __str__(self):
        return self.name
    
class ClassInfo(models.Model):
    name = models.CharField(max_length=45, unique=True)
    display_name = models.CharField(max_length=10, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.display_name

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
    phone_no = models.CharField(max_length=11)
    email = models.EmailField(blank=True, null=True)
    birth_certificate_no = models.IntegerField()
    religion_choice = (
        ('Islam', 'Islam'),
        ('Hinduism', 'Hinduism'),
        ('Buddhism', 'Buddhism'),
        ('Christianity', 'Christianity'),
        ('Others', 'Others')
    )
    religion = models.CharField(choices=religion_choice, max_length=45)
    nationality_choice = (
        ('Bangladeshi', 'Bangladeshi'),
        ('Others', 'Others')
    )
    nationality = models.CharField(choices=nationality_choice, max_length=45)

    def __str__(self):
        return self.name
class District(models.Model):
    name = models.CharField(max_length=45, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Upazilla(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Union(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class StudentAddressInfo(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.CASCADE)
    union = models.ForeignKey(Union, on_delete=models.CASCADE)
    village = models.TextField()

    def __str__(self):
        return self.village

class GuardianInfo(models.Model):
    father_name = models.CharField(max_length=100)
    father_phone_no = models.CharField(max_length=11)
    father_occupation_choice = (
        ('Agriculture', 'Agriculture'),
        ('Banker', 'Banker'),
        ('Business', 'Business'),
        ('Doctor', 'Doctor'),
        ('Farmer', 'Farmer'),
        ('Fisherman', 'Fisherman'),
        ('Public Service', 'Public Service'),
        ('Private Service', 'Private Service'),
        ('Shopkeeper', 'Shopkeeper'),
        ('Driver', 'Driver'),
        ('Worker', 'Worker'),
        ('N/A', 'N/A'),
    )
    father_occupation = models.CharField(choices=father_occupation_choice, max_length=45)
    father_yearly_income = models.IntegerField()
    mother_name = models.CharField(max_length=100)
    mother_phone_no = models.CharField(max_length=11)
    mother_occupation_choice = (
        ('Agriculture', 'Agriculture'),
        ('Banker', 'Banker'),
        ('Business', 'Business'),
        ('Doctor', 'Doctor'),
        ('Farmer', 'Farmer'),
        ('Fisherman', 'Fisherman'),
        ('Public Service', 'Public Service'),
        ('Private Service', 'Private Service'),
        ('Shopkeeper', 'Shopkeeper'),
        ('Driver', 'Driver'),
        ('Worker', 'Worker'),
        ('N/A', 'N/A'),
    )
    mother_occupation = models.CharField(choices=mother_occupation_choice, max_length=45)
    guardian_name = models.CharField(max_length=100)
    guardian_phone_no = models.CharField(max_length=11)
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
    group = models.CharField(max_length=45)
    gpa = models.CharField(max_length=10)
    board_roll = models.IntegerField()
    passing_year = models.IntegerField()

    def __str__(self):
        return self.institute_name

class PreviousAcademicCertificate(models.Model):
    birth_certificate = models.FileField(upload_to='documents/', blank=True)
    release_letter = models.FileField(upload_to='documents/', blank=True)
    testimonial = models.FileField(upload_to='documents/', blank=True)
    marksheet = models.FileField(upload_to='documents/', blank=True)
    stipen_certificate = models.FileField(upload_to='documents/', blank=True)
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
    address_info = models.ForeignKey(StudentAddressInfo, on_delete=models.CASCADE, null=True)
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
# class login(UserManager):
#     login_id = models.AutoField(primary_key=True)
#     def _create_user(self, email, password, **extra_fields):
#         email = self.normalize_email(email)
#         user = User(email=email, **extra_fields)
#         user.password = make_password(password)
#         user.save(using=self._db)
#         return user
    
# class User(AbstractUser):
#     GENDER = [("M", "Male"), ("F", "Female")]

#     user_id = models.AutoField(primary_key=True)
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=255)
#     phone = models.CharField(max_length=20)
#     address=models.TextField()
#     gender = models.CharField(max_length=1, choices=GENDER)
#     DOB=models.DateField()
#     DOJ=models.DateField()
#     profile_pic = models.ImageField()
#     login_id = models.ForeignKey(login,on_delete=models.CASCADE)
