
from django.http import HttpResponseRedirect,FileResponse 
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.shortcuts import render
from django.db import IntegrityError
from django.forms import modelformset_factory

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import PersonalInfoForm 
import csv
import logging

logger = logging.getLogger(__name__)


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('username')
        entered_password = request.POST.get('password')
        user = authenticate(request, email=email, password=entered_password)

        if user is not None:
                login(request, user)
                if user.role=='admin':
                  return redirect('hoddashboard')
                elif user.role=='teacher':
                    return redirect('teacherdashboard')
                elif user.role=='student':
                    return redirect('studentdashboard')
                else:
                   messages.error(request, 'Account is deactivated')
        else: 
            messages.error(request, 'Invalid login credentials')

        return redirect('login_page')

    return render(request, 'login/index.html')

def admin_profile(request, admin_id):
    # Fetch the CustomUser object for the given admin_id
    admin_user = get_object_or_404(CustomUser, pk=admin_id, role='admin')
    
    # Create a context dictionary to pass data to the template
    context = {
        'user': admin_user
    }
    
    # Render the template with the context data
    return render(request, 'hod/hodprofile.html', context)

def student_acprofile(request, student_id):
    # Fetch the CustomUser object for the given admin_id
    student_user = get_object_or_404(CustomUser, pk=student_id, role='student')
    
    # Create a context dictionary to pass data to the template
    context = {
        'user': student_user
    }
    
    # Render the template with the context data
    return render(request, 'student/studentprofile.html', context)

def teacher_acprofile(request, teacher_id):
    teacher_user = get_object_or_404(CustomUser, pk=teacher_id, role='teacher')
    
    context = {
        'user': teacher_user
    }
    
    # Render the template with the context data
    return render(request, 'teacher/teacherprofile.html', context)

def bulk_register(request):
    if request.method == 'POST':
        form = BulkRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.cleaned_data['user_file']
            try:
                with user_file.open() as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        email = row['email']
                        phone_no = row['phone_no']
                        user = User.objects.create_user(username=email, password=phone_no, email=email)
                        # Create PersonalInfo associated with this user
                        PersonalInfo.objects.create(email=email, phone_no=phone_no, user=user)
                messages.success(request, 'Bulk registration successful!')
            except Exception as e:
                messages.error(request, f'Bulk registration failed: {str(e)}')
            return redirect('hod_dashboard')
    else:
        form = BulkRegistrationForm()
    return render(request, 'registration/bulk_register.html', {'form': form})

def studentdashboard(request):
    user=request.user
    print(user)
    student = PersonalInfo.objects.all()
    context = {
        'student': student
    }
    return render(request,'student/student_dashboard.html',context)
from django.contrib.auth import authenticate, login






#----------------HOD-dashboard-----------#

def hoddashboard(request):
    context = {
        'admin': request.user,
    }
    return render(request, 'hod/hoddashboard.html', context)



def add_class(request):
    forms = ClassInfoForm()  # Initialize the form here
    class_obj = ClassInfo.objects.all()  # You can fetch all classes outside the POST block as well

    if request.method == 'POST':
        forms = ClassInfoForm(request.POST)  # Re-bind the form with POST data
        if forms.is_valid():
            new_name = forms.cleaned_data['name']
            new_display_name = forms.cleaned_data['display_name']

            new_class = ClassInfo(
                name=new_name,
                display_name=new_display_name
            )
            new_class.save()
            return redirect('add_class')

    context = {
        'forms': forms,  # No need for parentheses here
        'class_obj': class_obj,
        'success': True if request.method == 'POST' and forms.is_valid() else False
    }

    return render(request, 'hod/create_class.html', context)


def update_class(request, class_id):
    class_instance = get_object_or_404(ClassInfo, id=class_id)
    form = ClassInfoForm(instance=class_instance)
    
    if request.method == 'POST':
        form = ClassInfoForm(request.POST, instance=class_instance)
        if form.is_valid():
            form.save()
            return redirect('add_class')
    
    context = {
        'form': form,
    }
    return render(request, 'hod/update_classsection.html', context)

def delete_class(request, class_id):
    class_instance = get_object_or_404(ClassInfo, id=class_id)
    if request.method == 'POST':
        class_instance.is_deleted = True  # Soft delete
        class_instance.save()
        return redirect('add_class')
    
    context = {
        'class_obj': class_instance,
    }
    
    return render(request, 'hod/create_class.html', context)

def create_section(request):
    forms = SectionForm()
    error_message = None  # Initializing the error message

    if request.method == 'POST':
        forms = SectionForm(request.POST)
        if forms.is_valid():
            try:
                forms.save()
                return redirect('create-section')
            except IntegrityError:  # Catch the IntegrityError
                error_message = "A section with this name already exists."

    section = Section.objects.filter(is_deleted=False)
    context = {
        'forms': forms,
        'section': section,
        'error_message': error_message  # Add the error message to the context
    }
    return render(request, 'hod/create_classsection.html', context)

def update_section(request, section_id):
    section_instance = get_object_or_404(Section, id=section_id)
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section_instance)
        if form.is_valid():
            form.save()
            return redirect('create-section')
    else:
        form = SectionForm(instance=section_instance)
    return render(request, 'hod/update_classsection.html', {'form': form})

def delete_section(request, section_id):
    section_instance = get_object_or_404(Section, id=section_id)
    section_instance.delete()
    return redirect('create-section')

def create_guide_teacher(request):
    forms = GuideTeacherForm()
    if request.method == 'POST':
        forms = GuideTeacherForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('guide-teacher')
    guide_teacher = GuideTeacher.objects.all()
    context = {
        'forms': forms,
        'guide_teacher': guide_teacher
    }
    return render(request, 'hod/create_guideteacher.html', context)    

def create_session(request):
    forms = SessionForm()
    if request.method == 'POST':
        forms = SessionForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('create-session')
    session = Session.objects.filter(is_deleted=False)  # Only show non-deleted sessions
    context = {
        'forms': forms,
        'session': session
    }
    return render(request, 'hod/create_session.html', context)
def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    session.is_deleted = True
    session.save()
    return redirect('create-session')

def update_session(request, session_id):
    session_instance = get_object_or_404(Session, id=session_id)
    
    # If this is a POST request, process form data
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session_instance)

        if form.is_valid():
            form.save()
            return redirect('create-session')  # Redirect to your session list view

    # If this is a GET (or any other method), create the default form
    else:
        form = SessionForm(instance=session_instance)

    context = {
        'forms': form,
        'session_id': session_id,
    }

    return render(request, 'hod/create_session.html', context)

def class_registration(request):
    forms = ClassRegistrationForm()
    if request.method == 'POST':
        forms = ClassRegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('class-list')
    context = {'forms': forms}
    return render(request, 'hod/class_registration.html', context)

def class_list(request):
    register_class = ClassRegistration.objects.all()
    context = {'register_class': register_class}
    return render(request, 'hod/class_list.html', context)




def class_wise_student_registration(request):
    register_class = ClassRegistration.objects.all()
    context = {'register_class': register_class}
    return render(request, 'hod/hod_student/class-wise-student-registration.html', context)

def student_registration(request):
    academic_info_form = AcademicInfoForm(request.POST or None)
    personal_info_form = PersonalInfoForm(request.POST or None, request.FILES or None)
    guardian_info_form = GuardianInfoForm(request.POST or None)
    previous_academic_info_form = PreviousAcademicInfoForm(request.POST or None)
    previous_academic_certificate_form = PreviousAcademicCertificateForm(request.POST or None, request.FILES)

    if request.method == 'POST':
        if academic_info_form.is_valid() and personal_info_form.is_valid() and guardian_info_form.is_valid()  and previous_academic_info_form.is_valid() and previous_academic_certificate_form.is_valid():
            email = personal_info_form.cleaned_data.get('email')
            password = personal_info_form.cleaned_data.get('password')
            address = personal_info_form.cleaned_data.get('address')
            mobile = personal_info_form.cleaned_data.get('mobile')
            name = personal_info_form.cleaned_data.get('name')
            
            if CustomUser.objects.filter(email=email, role='student').exists():
                # Here you can add an error message indicating that a user with this email already exists
                messages.error(request, 'A student with this email already exists.')
            else:
                user = CustomUser.objects.create_user(name=name,email=email, password=password,address=address,mobile=mobile, role='student')
                s1 = personal_info_form.save()
                s1.user = user  # associate the user with the PersonalInfo model
                s1.save()
                s3 = guardian_info_form.save()
                s5 = previous_academic_info_form.save()
                s6 = previous_academic_certificate_form.save()
                academic_info = academic_info_form.save(commit=False)
                academic_info.personal_info = s1
                academic_info.guardian_info = s3
                academic_info.previous_academic_info = s5
                academic_info.previous_academic_certificate = s6
                academic_info.save()
                return redirect('student-list')

    context = {
        'academic_info_form': academic_info_form,
        'personal_info_form': personal_info_form,
        'guardian_info_form': guardian_info_form,
        'previous_academic_info_form': previous_academic_info_form,
        'previous_academic_certificate_form': previous_academic_certificate_form
    }
    return render(request, 'hod/hod_student/student-registration.html', context)

def student_list(request):
    # Use select_related to prefetch related data
    student = AcademicInfo.objects.select_related('personal_info__user').filter(is_delete=False).order_by('-id')
    context = {'student': student}
    return render(request, 'hod/hod_student/student-list.html', context)

def student_profile(request, reg_no):
    student = AcademicInfo.objects.get(registration_no=reg_no)
    context = {
        'student': student
    }
    return render(request, 'hod/hod_student/student-profile.html', context)

def student_edit(request, reg_no):
    student = AcademicInfo.objects.get(registration_no=reg_no)
    academic_info_form = AcademicInfoForm(instance=student)
    personal_info_form = PersonalInfoForm(instance=student.personal_info)
    guardian_info_form = GuardianInfoForm(instance=student.guardian_info)
    previous_academic_info_form = PreviousAcademicInfoForm(instance=student.previous_academic_info)
    previous_academic_certificate_form = PreviousAcademicCertificateForm(instance=student.previous_academic_certificate)

    if request.method == 'POST':
        academic_info_form = AcademicInfoForm(request.POST, instance=student)
        personal_info_form = PersonalInfoForm(request.POST, request.FILES, instance=student.personal_info)
        guardian_info_form = GuardianInfoForm(request.POST, instance=student.guardian_info)
        previous_academic_info_form = PreviousAcademicInfoForm(request.POST, instance=student.previous_academic_info)
        previous_academic_certificate_form = PreviousAcademicCertificateForm(request.POST, request.FILES, instance=student.previous_academic_certificate)
        if academic_info_form.is_valid() and personal_info_form.is_valid() and guardian_info_form.is_valid() and previous_academic_info_form.is_valid() and previous_academic_certificate_form.is_valid():
            s1 = personal_info_form.save()
            s3 = guardian_info_form.save()
            s5 = previous_academic_info_form.save()
            s6 = previous_academic_certificate_form.save()
            academic_info = academic_info_form.save(commit=False)
            academic_info.personal_info = s1
            academic_info.guardian_info = s3
            academic_info.previous_academic_info = s5
            academic_info.previous_academic_certificate = s6
            academic_info.save()
            return redirect('student-list')

    context = {
        'academic_info_form': academic_info_form,
        'personal_info_form': personal_info_form,
        'guardian_info_form': guardian_info_form,
        'previous_academic_info_form': previous_academic_info_form,
        'previous_academic_certificate_form': previous_academic_certificate_form
    }
    return render(request, 'hod/hod_student/student-edit.html', context)

def student_delete(request, reg_no):
    student = AcademicInfo.objects.get(registration_no=reg_no)
    student.is_delete = True
    student.save()
    return redirect('student-list')

def student_search(request):
    forms = StudentSearchForm()
    cls_name = request.GET.get('class_info', None)
    reg_no = request.GET.get('registration_no', None)
    if cls_name:
        student = AcademicInfo.objects.filter(class_info=cls_name)
        if reg_no:
            student = student.filter(registration_no=reg_no)
        context = {
            'forms': forms,
            'student': student
        }
        return render(request, 'hod/hod_student/student-search.html', context)
    else:
        student = AcademicInfo.objects.filter(registration_no=reg_no)
        context = {
            'forms': forms,
            'student': student
        }
        return render(request, 'hod/hod_student/student-search.html', context)
    


def enrolled_student(request):
    forms = EnrolledStudentForm()
    cls = request.GET.get('class_name', None)
    student = AcademicInfo.objects.filter(class_info=cls, status='not enroll')
    context = {
        'forms': forms,
        'student': student
    }
    return render(request, 'hod/hod_student/enrolled.html', context)

def student_enrolled(request, reg):
    student = AcademicInfo.objects.get(registration_no=reg)
    forms = StudentEnrollForm()
    if request.method == 'POST':
        forms = StudentEnrollForm(request.POST)
        if forms.is_valid():
            roll = forms.cleaned_data['roll_no']
            class_name = forms.cleaned_data['class_name']
            EnrolledStudent.objects.create(class_name=class_name, student=student, roll=roll)
            student.status = 'enrolled'
            student.save()
            return redirect('enrolled-student-list')
    context = {
        'student': student,
        'forms': forms
    }
    return render(request, 'hod/hod_student/student-enrolled.html', context)

def enrolled_student_list(request):
    student = EnrolledStudent.objects.all()
    forms = SearchEnrolledStudentForm()
    class_name = request.GET.get('reg_class', None)
    roll = request.GET.get('roll_no', None)
    if class_name:
        student = EnrolledStudent.objects.filter(class_name=class_name)
        context = {
            'forms': forms,
            'student': student
        }
        return render(request, 'hod/hod_student/enrolled-student-list.html', context)
    context = {
        'forms': forms,
        'student': student
    }
    return render(request, 'hod/hod_student/enrolled-student-list.html', context)



def teacherdashboard(request):
    user=request.user
    print(user)
    teacher = TeacherPersonalInfo.objects.all()
    context = {
        'teacher': teacher
    }
    return render(request,'teacher/teacher_dashboard.html',context)




def user_logout(request):
    logout(request)
    return redirect('/')

def teacher_registration(request):
    form = TeacherPersonalInfoForm(request.POST or None, request.FILES or None)
    education_form = EducationInfoForm(request.POST or None)
    training_form = TrainingInfoForm(request.POST or None)
    experience_form = ExperienceInfoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid() and education_form.is_valid() and training_form.is_valid() and experience_form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            address = form.cleaned_data.get('address')
            mobile = form.cleaned_data.get('phone_no')
            name = form.cleaned_data.get('name')
            if CustomUser.objects.filter(email=email, role='teacher').exists():
                messages.error(request, 'A student with this email already exists.')
            else:
                user = CustomUser.objects.create_user(name=name, email=email, password=password, address=address, mobile=mobile, role='teacher')

                # Associate the user with the TeacherPersonalInfo instance before saving it.
                personal_info = form.save(commit=False)
                personal_info.user = user

                # Save the associated models
                education_info = education_form.save()
                training_info = training_form.save()
                experience_info = experience_form.save()

                personal_info.education = education_info
                personal_info.training = training_info
                personal_info.experience = experience_info
                personal_info.save()

                return redirect('teacher-list')

    context = {
        'form': form,
        'education_form': education_form,
        'training_form': training_form,
        'experience_form': experience_form
    }
    return render(request, 'hod/teacher-registration.html', context)



def teacher_list(request):
    teacher = TeacherPersonalInfo.objects.filter(is_delete=False)
  
    context = {'teacher': teacher}
    return render(request, 'hod/teacher-list.html', context)

def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)
    context = {
        'teacher': teacher
    }
    return render(request, 'hod/teacher-profile.html', context)

def teacher_delete(request, teacher_id):
    teacher = TeacherPersonalInfo.objects.get(id=teacher_id)
    teacher.is_delete = True
    teacher.save()
    return redirect('teacher-list')

def teacher_edit(request, teacher_id):
    teacher = TeacherPersonalInfo.objects.get(id=teacher_id)
    form = TeacherPersonalInfoForm(instance=teacher)
    education_form = EducationInfoForm(instance=teacher.education)
    training_form = TrainingInfoForm(instance=teacher.training)
    experience_form = ExperienceInfoForm(instance=teacher.experience)
    if request.method == 'POST':
        form = TeacherPersonalInfoForm(request.POST, request.FILES, instance=teacher)
        education_form = EducationInfoForm(request.POST, instance=teacher.education)
        training_form = TrainingInfoForm(request.POST, instance=teacher.training)
        experience_form = ExperienceInfoForm(request.POST, instance=teacher.experience)
        if form.is_valid() and education_form.is_valid() and training_form.is_valid()  and experience_form.is_valid():
            education_info = education_form.save()
            training_info = training_form.save()
            experience_info = experience_form.save()
            personal_info = form.save(commit=False)
            personal_info.education = education_info
            personal_info.training = training_info
            personal_info.experience = experience_info
            personal_info.save()
            return redirect('teacher-list')
    context = {
        'form': form,
        'education_form': education_form,
        'training_form': training_form,
        'experience_form': experience_form
    }
    return render(request, 'hod/teacher-edit.html', context)


def add_designation(request):
    forms = AddDesignationForm()
    if request.method == 'POST':
        forms = AddDesignationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('designation')
    designation = Designation.objects.all()
    context = {'forms': forms, 'designation': designation}
    return render(request, 'hod/designation.html', context)

def update_designation(request, designation_id):
    instance = get_object_or_404(Designation, id=designation_id)
    forms = AddDesignationForm(request.POST or None, instance=instance)
    
    if request.method == 'POST':
        if forms.is_valid():
            forms.save()
            return redirect('designation') # Redirect back to the designation page
    
    context = {'forms': forms}
    return render(request, 'hod/designation.html', context)

        
#------------teacher dashborad---#
def class_student(request):
    # Assuming user is logged in and is a GuideTeacher
    try:
        guide_teacher = GuideTeacher.objects.get(name=request.user.teacherpersonalinfo)
    except GuideTeacher.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not a guide teacher!'})

    class_registrations = ClassRegistration.objects.filter(guide_teacher=guide_teacher)
    students = EnrolledStudent.objects.filter(class_name__in=class_registrations)

    AttendanceFormSet = modelformset_factory(StudentAttendance, form=StudentAttendanceForm, extra=0)

    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            # Redirect to a success page or the same page after saving
            return redirect('class_student')
    else:
        queryset = StudentAttendance.objects.filter(student__in=students, date=timezone.now())
        if not queryset.exists():
            queryset = [StudentAttendance(student=student, date=timezone.now()) for student in students]
        formset = AttendanceFormSet(queryset=queryset)

    context = {
        'formset': formset,
        'students': students
    }
    return render(request, 'teacher/class_student.html', context)

def mark_attendance(request):
   return render(request,'teacher/attendance/mark_attendace.html')



def add_resource(request):
    # Assuming the teacher is the logged-in user
    teacher = TeacherPersonalInfo.objects.get(user=request.user)

    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            # Set the class registration for the resource based on the teacher's classes
            resource.class_registration = ClassRegistration.objects.get(guide_teacher=teacher)
            resource.save()
            return redirect('teacher/index_resource.html')
    else:
        form = ResourceForm()
    return render(request, 'teacher/add_resource.html', {'form': form})

def view_resource():
 return HttpResponseRedirect(reverse('index_resource'))

def edit_resource(request):
    if request.method == 'POST':
      resource = Resource.objects.get(pk=id)
      form = ResourceForm(request.POST, instance=resource)
      if form.is_valid():
        form.save()
      return render(request, 'teacher/edit_resource.html', {
        'form': form,
        'success': True
      })
    else:
      resource = Resource.objects.get(pk=id)
      form = ResourceForm(instance=resource)
    return render(request, 'teacher/edit_resource.html', {
    'form': form
  })



def delete_resource(request):
    if request.method == 'POST':
     resource = Resource.objects.get(pk=id)
     resource.delete()
    return HttpResponseRedirect(reverse('index_resource'))


def uploadresource(request):
   return render(request,'teacher/resource.html')


def index_resource(request):
   return render(request,'teacher/index_resource.html')


#--------------student dashboard-------#
def studentdashboard(request):
   return render(request,'student/student_dashboard.html')

def student_resources(request):
    student_class = EnrolledStudent.objects.get(student__user=request.user).class_name
    resources = Resource.objects.filter(class_registration=student_class)
    return render(request, 'student/resources.html', {'resources': resources})

def downloadresource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    response = FileResponse(resource.resource_file)
    return response

def editprofile(request):
   return render(request,'student/edit-profile.html')


def logout_user(request):
    print('Logged Out')
    logout(request)
    return redirect('/')

