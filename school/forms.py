from django import forms
from .models import *
from datetime import datetime

import os
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms

def validate_pdf_file(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only PDF files are allowed.')
    
def validate_only_alphabets(value):
     if not value.replace(" ", "").isalpha():
        raise ValidationError('Only alphabets and spaces are allowed.')

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_no = forms.CharField(max_length=10, required=True,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['email', 'phone_no']

class ResourceForm(forms.ModelForm):
  class Meta:
    model = Resource
    fields = '__all__'
    labels = {
      'resouce_id': 'resource_id',
      'resource_title': 'resource_title',
      'teacher_name':'teacher_name',
      'resouce_file': 'resource_file',
      'file_type':'file Type',
      'description':'Description',
      
    }
    widgets = {
      'resource_id': forms.NumberInput(attrs={'class': 'form-control'}),
      'resource_title': forms.TextInput(attrs={'class': 'form-control'}),
      'resource_file': forms.FileInput(attrs={'class': 'form-control'}),
      'file_type':forms.TextInput(attrs={'class': 'form-control'}),
      'description':forms.TextInput(attrs={'class': 'form-control'}),
    }


class ClassInfoForm(forms.ModelForm):
    class Meta:
        model = ClassInfo
        fields = '__all__'
        exclued='is_deleted'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Check if the name contains only alphabets
        validate_only_alphabets(name)
        
        # Check for minimum length
        if len(name) < 3:
            raise ValidationError("The name should be at least 3 characters long.")
            
        return name

    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name')
        
        # Check if the display_name contains only alphabets
        validate_only_alphabets(display_name)
        
        # Check for specific length range
        if not (2 <= len(display_name) <= 10):
            raise ValidationError("The display name should be between 2 and 5 characters long.")
            
        return display_name

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
        exclude = ['is_deleted']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Validate the name with our custom validator
        validate_only_alphabets(name)

        return name

class GuideTeacherForm(forms.ModelForm):
    class Meta:
        model = GuideTeacher
        fields = '__all__'
        exclude = ['is_deleted']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Validate the name with our custom validator
        validate_only_alphabets(name)

        return name
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if GuideTeacher.objects.filter(name=name).exists():
            raise ValidationError('This guide teacher is already selected.')
        return name

# Generating a list of years from 2000 to the current year
YEARS = [(year, year) for year in range(2000, datetime.now().year + 1)]

class SessionForm(forms.ModelForm):
    # Override the name field to use ChoiceField
    name = forms.ChoiceField(choices=YEARS, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Session
        fields = '__all__'
        exclude = ['is_deleted']  # Exclude the is_deleted field

class ClassRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = ClassRegistration
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
            'guide_teacher': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Validate the name with our custom validator
        validate_only_alphabets(name)

        return name
class AcademicInfoForm(forms.ModelForm):
    class Meta:
        model = AcademicInfo
        exclude = ['registration_no', 'status', 'personal_info', 'guardian_info',  'previous_academic_info', 'previous_academic_certificate', 'is_delete']
        widgets = {
            'class_info': forms.Select(attrs={'class': 'form-control'})
        }

class PersonalInfoForm(forms.ModelForm):
    role = forms.ChoiceField(choices=CustomUser.USER_ROLES, initial='student')
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Name')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Passwprd')
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Address')
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Phone')



    class Meta:
        model = PersonalInfo
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),


           
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Validate the name with our custom validator
        validate_only_alphabets(name)

        return name
    def __init__(self, *args, **kwargs):
        super(PersonalInfoForm, self).__init__(*args, **kwargs)
        self.fields['role'].initial = 'student' 
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
    
        if password and password_confirm and password != password_confirm:
           self.add_error('password_confirm', "Passwords don't match")
        return cleaned_data
class GuardianInfoForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed."
    )
    father_phone_no = forms.CharField(validators=[phone_regex], widget=forms.TextInput(attrs={'class': 'form-control'}))  # Use CharField
    mother_phone_no = forms.CharField(validators=[phone_regex], widget=forms.TextInput(attrs={'class': 'form-control'}))  # Use CharField
    guardian_phone_no = forms.CharField(validators=[phone_regex], widget=forms.TextInput(attrs={'class': 'form-control'}))  # Use CharField
    
    class Meta:
        model = GuardianInfo
        fields = '__all__'
        exclude=['student'] 
        widgets = {
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship_with_student': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_name(self):
        father_name = self.cleaned_data.get('father_name')
        mother_name=self.cleaned_data.get('mother_name')
        # Validate the name with our custom validator
        validate_only_alphabets(father_name)
        validate_only_alphabets(mother_name)

        return father_name and mother_name
    
 
class PreviousAcademicInfoForm(forms.ModelForm):
    passing_year= forms.ChoiceField(choices=YEARS, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = PreviousAcademicInfo
        fields = '__all__'
        widgets = {
            'institute_name': forms.TextInput(attrs={'class': 'form-control'}),
            'name_of_exam': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.TextInput(attrs={'class': 'form-control'}),
            'board_roll': forms.TextInput(attrs={'class': 'form-control'}),
           
        }
    def clean_name(self):
    
        institute_name=self.cleaned_data.get('institute_name')
        # Validate the name with our custom validator
        validate_only_alphabets(institute_name)

        return institute_name

class PreviousAcademicCertificateForm(forms.ModelForm):
    marksheet = forms.FileField(validators=[validate_pdf_file])
    other_certificate = forms.FileField(validators=[validate_pdf_file])
    

    class Meta:
        model = PreviousAcademicCertificate
        fields = '__all__'
    
class StudentSearchForm(forms.Form):
    class_info = forms.ModelChoiceField(required=False, queryset=ClassInfo.objects.all())
    registration_no = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Registration No', 'aria-controls': 'DataTables_Table_0'}))

class EnrolledStudentForm(forms.Form):
    class_name = forms.ModelChoiceField(queryset=ClassInfo.objects.all())

class StudentEnrollForm(forms.Form):
    class_name = forms.ModelChoiceField(queryset=ClassRegistration.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    roll_no = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Roll', 'class': 'form-control'}))

class SearchEnrolledStudentForm(forms.Form):
    reg_class = forms.ModelChoiceField(queryset=ClassRegistration.objects.all())
    roll_no = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Enter Roll'}))



class SearchEnrolledStudentForm(forms.Form):
    reg_class = forms.ModelChoiceField(queryset=ClassRegistration.objects.all())


class TeacherPersonalInfoForm(forms.ModelForm):
  
    role = forms.ChoiceField(choices=CustomUser.USER_ROLES, initial='teacher')
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Name')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Address')
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Phone')
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), label='Photo')


    def __init__(self, *args, **kwargs):
      super(TeacherPersonalInfoForm, self).__init__(*args, **kwargs)

    # Check if the instance has been saved and associated with a user before setting initial data
      if self.instance.pk and self.instance.user:
        self.fields['name'].initial = self.instance.user.name
        self.fields['email'].initial = self.instance.user.email
        # Don't set the initial password for security reasons
        self.fields['address'].initial = self.instance.user.address
        self.fields['mobile'].initial = self.instance.user.mobile


    class Meta:
        model = TeacherPersonalInfo
        exclude = {'education', 'training', 'experience', 'is_delete', 'user'}
        fields = ['name', 'email', 'password', 'address', 'mobile', 'photo', 'date_of_birth', 'gender', 'blood_group']
        
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            main, ext = os.path.splitext(photo.name)
            if not ext.lower() in ['.jpg', '.jpeg']:
                raise ValidationError('Supported photo formats are: .jpg, .jpeg')
        return photo
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
    
        if password and password_confirm and password != password_confirm:
           self.add_error('password_confirm', "Passwords don't match")
        return cleaned_data
    def clean_name(self):
        # Fetch the name value from the cleaned_data
        name = self.cleaned_data.get('name')

        # Check if the name has any digits
        if any(char.isdigit() for char in name):
            raise ValidationError("Name should not contain any numbers.")

        # Check if the name contains only alphabets and spaces
        if not re.match("^[A-Za-z\s]+$", name):
            raise ValidationError("Name should only contain alphabets and spaces.")

        return name
    def save(self, commit=True):
        teacher = super(TeacherPersonalInfoForm, self).save(commit=False)

        # Create or update the associated user
        user_email = self.cleaned_data['email']
        user_password = self.cleaned_data['password']

        # Since email is unique, you should check if a user with that email already exists
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(username=user_email, email=user_email, password=user_password)

        teacher.user = user

        if commit:
            user.save()
            teacher.save()

        return teacher

YEARS = [(year, year) for year in range(2000, datetime.now().year + 1)]

class EducationInfoForm(forms.ModelForm):
    passing_year = forms.ChoiceField(choices=YEARS, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = EducationInfo
        fields = '__all__'
        widgets = {
            'name_of_exam': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_name_of_exam(self):
        name_of_exam = self.cleaned_data.get('name_of_exam')

        # Ensure the name of the exam isn't just a series of numbers.
        if name_of_exam.isdigit():
            raise ValidationError("The name of the exam shouldn't be just numbers.")

        # Ensure the name isn't too short.
        if len(name_of_exam) < 3:
            raise ValidationError("The name of the exam should be at least 3 characters long.")
        
        if any(char.isdigit() for char in name_of_exam):
            raise ValidationError("Name should not contain any numbers.")
        
        return name_of_exam


class TrainingInfoForm(forms.ModelForm):
    year = forms.ChoiceField(choices=YEARS, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = TrainingInfo
        fields = '__all__'
        widgets = {
            'training_name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_training_name(self):
        training_name = self.cleaned_data.get('training_name')

        # Ensure the training_name contains only alphabets and possibly spaces.
        if not training_name.replace(" ", "").isalpha():
            raise ValidationError("The training name should only contain alphabets and spaces.")

        return training_name


class ExperienceInfoForm(forms.ModelForm):
    class Meta:
        model = ExperienceInfo
        fields = '__all__'
        widgets = {
            'institute_name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from django.core.exceptions import ValidationError
import re

class AddDesignationForm(forms.ModelForm):
    
    class Meta:
        model = Designation
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_name(self):
        # Fetch the name value from the cleaned_data
        name = self.cleaned_data.get('name')

        # Check if the name has any digits
        if any(char.isdigit() for char in name):
            raise ValidationError("Name should not contain any numbers.")

        # Check if the name contains only alphabets and spaces
        if not re.match("^[A-Za-z\s]+$", name):
            raise ValidationError("Name should only contain alphabets and spaces.")

        return name
