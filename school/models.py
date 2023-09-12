from django.db import models
from django.core.validators import RegexValidator


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
