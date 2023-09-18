from django import forms
from .models import *
from datetime import datetime

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

class ClassInfoForm(forms.ModelForm):
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
        exclude = ['is_deleted']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GuideTeacherForm(forms.ModelForm):
    class Meta:
        model = GuideTeacher
        fields = '__all__'
        exclude = ['is_deleted']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
        }


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
class AcademicInfoForm(forms.ModelForm):
    class Meta:
        model = AcademicInfo
        exclude = ['registration_no', 'status', 'personal_info', 'address_info', 'guardian_info', 'emergency_contact_info', 'previous_academic_info', 'previous_academic_certificate', 'is_delete']
        widgets = {
            'class_info': forms.Select(attrs={'class': 'form-control'})
        }

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_certificate_no': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'})
        }

class StudentAddressInfoForm(forms.ModelForm):
    class Meta:
        model = StudentAddressInfo
        fields = '__all__'
        widgets = {
            'district': forms.Select(attrs={'class': 'form-control'}),
            'upazilla': forms.Select(attrs={'class': 'form-control'}),
            'union': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'})
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['upazilla'].queryset = Upazilla.objects.none()

            if 'upazilla' in self.data:
                try:
                    district_id = int(self.data.get('district'))
                    self.fields['upazilla'].queryset = Upazilla.objects.filter(district_id=district_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['upazilla'].queryset = self.instance.district.upazilla_set.order_by('name')

            self.fields['union'].queryset = Union.objects.none()

            if 'union' in self.data:
                try:
                    upazilla_id = int(self.data.get('upazilla'))
                    self.fields['union'].queryset = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['union'].queryset = self.instance.upazilla.union_set.order_by('name')


class GuardianInfoForm(forms.ModelForm):
    class Meta:
        model = GuardianInfo
        fields = '__all__'
        widgets = {
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'father_occupation': forms.Select(attrs={'class': 'form-control'}),
            'father_yearly_income': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_occupation': forms.Select(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship_with_student': forms.Select(attrs={'class': 'form-control'}),
        }

class EmergencyContactDetailsForm(forms.ModelForm):
    class Meta:
        model = EmergencyContactDetails
        fields = '__all__'
        widgets = {
            'emergency_guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'relationship_with_student': forms.Select(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PreviousAcademicInfoForm(forms.ModelForm):
    class Meta:
        model = PreviousAcademicInfo
        fields = '__all__'
        widgets = {
            'institute_name': forms.TextInput(attrs={'class': 'form-control'}),
            'name_of_exam': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.TextInput(attrs={'class': 'form-control'}),
            'board_roll': forms.TextInput(attrs={'class': 'form-control'}),
            'passing_year': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PreviousAcademicCertificateForm(forms.ModelForm):
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


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UpazillaForm(forms.ModelForm):
    class Meta:
        model = Upazilla
        fields = '__all__'
        widgets = {
            'district': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UnionForm(forms.ModelForm):
    class Meta:
        model = Union
        fields = '__all__'
        widgets = {
            'district': forms.Select(attrs={'class': 'form-control'}),
            'upazilla': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SearchEnrolledStudentForm(forms.Form):
    reg_class = forms.ModelChoiceField(queryset=ClassRegistration.objects.all())