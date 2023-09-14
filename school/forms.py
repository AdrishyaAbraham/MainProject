from django import forms
from .models import Student, Teacher, Resource,Class,Section,GuideTeacher,Session,ClassRegistration


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_number', 'name', 'email','address','phone_number','gender', 'dob','doj','fathername','father_contact','mothername','mother_contact']
        labels = {
            'student_number': 'Student Number',
            'name': 'Name',
            'email': 'Email',
            'address':'Address',
            'phone_number': 'Phone Number',
            'gender':'Gender',
            'dob': 'Date Of Birth',
            'doj':'Date of Joining',
            'fathername':'Father Name',
            'father_contact':'Father Contact Number',
            'mothername':'Mother Name',
            'mother_contact':'Mother Contact Number',
        }
        widgets = {
            'student_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender':forms.RadioSelect(),
            'dob': forms.DateInput(attrs={'class': 'form-control'},format='%Y-%m-%d'),
            'doj':forms.DateInput(attrs={'class': 'form-control'}),
            'fathername':forms.TextInput(attrs={'class': 'form-control'}),
            'father_contact':forms.TextInput(attrs={'class': 'form-control'}),
            'mothername':forms.TextInput(attrs={'class': 'form-control'}),
            'mother_contact':forms.TextInput(attrs={'class': 'form-control'}),
        }
        input_formats = {
            'dob': ['%Y-%m-%d']
        }

class TeacherForm(forms.ModelForm):
  class Meta:
    model = Teacher
    fields = ['teacher_number', 'name', 'email','address','phone_number','gender','dob','doj']
    labels = {
      'teacher_number': 'Teacher Number',
      'name': 'Name',
      'email': 'Email',
      'address':'Address',
      'phone_number': 'Phone Number',
      'gender':'Gender',
      'dob':'Date of Birth',
      'doj':'Date of Joining',

      
    }
    widgets = {
      'teacher_number': forms.NumberInput(attrs={'class': 'form-control'}),
      'name': forms.TextInput(attrs={'class': 'form-control'}),
      'email': forms.EmailInput(attrs={'class': 'form-control'}),
      'address': forms.TextInput(attrs={'class': 'form-control'}),
      'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
      'gender': forms.RadioSelect(),
      'dob': forms.DateInput(attrs={'class': 'form-control'}),
      'doj': forms.DateInput(attrs={'class': 'form-control'}),

    }


class ResourceForm(forms.ModelForm):
  class Meta:
    model = Resource
    fields = ['resource_id', 'resource_title', 'resource_file','file_type','description','uploaded_date']
    labels = {
      'resouce_id': 'resource_id',
      'resource_title': 'resource_title',
      'resouce_file': 'resource_file',
      'file_type':'file Type',
      'description':'Description',
      'uploaded_date':'uploaded date',
      
    }
    widgets = {
      'resource_id': forms.NumberInput(attrs={'class': 'form-control'}),
      'resource_title': forms.TextInput(attrs={'class': 'form-control'}),
      'resource_file': forms.FileInput(attrs={'class': 'form-control'}),
      'file_type':forms.TextInput(attrs={'class': 'form-control'}),
      'description':forms.TextInput(attrs={'class': 'form-control'}),
      'uploaded_date':forms.DateInput(attrs={'class': 'form-control'}),
    }

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GuideTeacherForm(forms.ModelForm):
    class Meta:
        model = GuideTeacher
        fields = '__all__'
        labels={'name':'Year'}
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
        }

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'name': forms.NumberInput(attrs={'class': 'form-control'}),
        }

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
