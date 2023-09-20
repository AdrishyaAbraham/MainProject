from django import forms
from . import models
import os
from datetime import datetime
from django.core.validators import RegexValidator

class PersonalInfoForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\d{10}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed."
    )
    phone_no = forms.CharField(validators=[phone_regex], widget=forms.TextInput(attrs={'class': 'form-control'}))  # Use CharField
    
    class Meta:
        model = models.PersonalInfo
        exclude = { 'education', 'training',  'experience', 'is_delete'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            main, ext = os.path.splitext(photo.name)
            if not ext.lower() in ['.jpg', '.jpeg']:
                raise ValidationError('Supported photo formats are: .jpg, .jpeg')
        return photo

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


YEARS = [(year, year) for year in range(2000, datetime.now().year + 1)]

class EducationInfoForm(forms.ModelForm):
    passing_year = forms.ChoiceField(choices=YEARS, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = models.EducationInfo
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
        model = models.TrainingInfo
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
        model = models.ExperienceInfo
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
        model = models.Designation
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
