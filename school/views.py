
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect,FileResponse 
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User

from onlineexam.views import *
from .models import *
from .forms import *
from django.shortcuts import render
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login
import csv
import logging
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

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
                elif user.role=='parent':
                    return redirect('parentdashboard')
                elif user.role=='priest':
                    return redirect('priestdashboard')
                else:
                   messages.error(request, 'Account is deactivated')
        else: 
            messages.error(request, 'Invalid login credentials')

        return redirect('login_page')

    return render(request, 'login/index.html')

@never_cache
@login_required(login_url='login_page')
def admin_profile(request, admin_id):
    # Fetch the CustomUser object for the given admin_id
    admin_user = get_object_or_404(CustomUser, pk=admin_id, role='admin')
    
    # Create a context dictionary to pass data to the template
    context = {
        'user': admin_user
    }
    
    # Render the template with the context data
    return render(request, 'hod/hodprofile.html', context)


@never_cache
@login_required(login_url='login_page')
def student_acprofile(request, student_id):
    # Fetch the CustomUser object for the given admin_id
    student_user = get_object_or_404(CustomUser, pk=student_id, role='student')
    
    # Create a context dictionary to pass data to the template
    context = {
        'user': student_user
    }
    
    # Render the template with the context data
    return render(request, 'student/studentprofile.html', context)

@never_cache
@login_required(login_url='login_page')
def teacher_acprofile(request, teacher_id):
    teacher_user = get_object_or_404(CustomUser, pk=teacher_id, role='teacher')
    
    context = {
        'user': teacher_user
    }
    
    # Render the template with the context data
    return render(request, 'teacher/teacherprofile.html', context)

@never_cache
@login_required(login_url='login_page')
def parent_acprofile(request, parent_id):
    parent_user = get_object_or_404(CustomUser, pk=parent_id, role='parent')
    
    context = {
        'user': parent_user
    }
    
    # Render the template with the context data
    return render(request, 'parent/parentprofile.html', context)

@never_cache
@login_required(login_url='login_page')
def priest_acprofile(request, priest_id):
    priest_user = get_object_or_404(CustomUser, pk=priest_id, role='priest')
    
    context = {
        'user': priest_user
    }
    
    # Render the template with the context data
    return render(request, 'priest/priestprofile.html', context)

@never_cache
@login_required(login_url='login_page')
def logout_user(request):
    print('Logged Out')
    logout(request)
    return redirect('/')

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

@never_cache
@login_required(login_url='login_page')
def studentdashboard(request):
    user=request.user
    print(user)
    student = PersonalInfo.objects.all()
    latest_submission = StudentExamSubmission.objects.filter(student=student).order_by('-submission_time').first()

    context = {
        'student': student,
        'submission_id': latest_submission.id if latest_submission else None,
    }
    return render(request,'student/student_dashboard.html',context)

from django.contrib.auth import authenticate, login




#----------------HOD-dashboard-----------#
@never_cache
@login_required(login_url='login_page')
def hoddashboard(request):
    exam_schedule = ExamSchedule.objects.first()
    registrations = Registration.objects.filter(student=request.user)
    
    context = {
        'exam_schedule': exam_schedule,
        'admin': request.user,
        'registrations': registrations,  # Include registrations in the context
    }
    return render(request, 'hod/hoddashboard.html', context)

@never_cache
@login_required(login_url='login_page')
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

@never_cache
@login_required
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

@never_cache
@login_required
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

@never_cache
@login_required
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

@never_cache
@login_required
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

@login_required
def delete_section(request, section_id):
    section_instance = get_object_or_404(Section, id=section_id)
    section_instance.delete()
    return redirect('create-section')

@login_required
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

@login_required
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
@login_required
def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    session.is_deleted = True
    session.save()
    return redirect('create-session')

@login_required
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

@login_required
def class_registration(request):
    forms = ClassRegistrationForm()
    if request.method == 'POST':
        forms = ClassRegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('class-list')
    context = {'forms': forms}
    return render(request, 'hod/class_registration.html', context)

@login_required
def class_list(request):
    register_class = ClassRegistration.objects.all()
    context = {'register_class': register_class}
    return render(request, 'hod/class_list.html', context)



@login_required
def class_wise_student_registration(request):
    register_class = ClassRegistration.objects.all()
    context = {'register_class': register_class}
    return render(request, 'hod/hod_student/class-wise-student-registration.html', context)

@login_required
def student_registration(request):
    academic_info_form = AcademicInfoForm(request.POST or None)
    personal_info_form = PersonalInfoForm(request.POST or None, request.FILES or None)
    guardian_info_form = GuardianInfoForm(request.POST or None)
    previous_academic_info_form = PreviousAcademicInfoForm(request.POST or None)
    previous_academic_certificate_form = PreviousAcademicCertificateForm(request.POST or None, request.FILES)

    if request.method == 'POST':
        if all([academic_info_form.is_valid(), personal_info_form.is_valid(), guardian_info_form.is_valid(), 
                previous_academic_info_form.is_valid(), previous_academic_certificate_form.is_valid()]):

            student_email = personal_info_form.cleaned_data.get('email')
            parent_email = guardian_info_form.cleaned_data.get('parent_email')

            father_name = guardian_info_form.cleaned_data.get('father_name')
            if CustomUser.objects.filter(email=student_email).exists():
                messages.error(request, 'A user with this student email already exists.')
            elif CustomUser.objects.filter(email=parent_email).exists():
                messages.error(request, 'A user with this parent email already exists.')
            else:
                # Common data
                password = personal_info_form.cleaned_data.get('password')
                address = personal_info_form.cleaned_data.get('address')
                mobile = personal_info_form.cleaned_data.get('mobile')
                name = personal_info_form.cleaned_data.get('name')

                # Create parent user
                parent_user = CustomUser.objects.create_user(name=father_name, email=parent_email, password=password, address=address, mobile=mobile, role='parent')
                guardian = guardian_info_form.save(commit=False)
                guardian.user = parent_user
                guardian.save()

                # Create student user
                student_user = CustomUser.objects.create_user(name=name, email=student_email, password=password, address=address, mobile=mobile, role='student')
                student_personal_info = personal_info_form.save(commit=False)
                student_personal_info.user = student_user
                student_personal_info.guardian = guardian  # Link the student to the guardian
                student_personal_info.save()

                                
                prev_academic_info = previous_academic_info_form.save()
                prev_academic_cert = previous_academic_certificate_form.save()

                academic_info = academic_info_form.save(commit=False)
                academic_info.personal_info = student_personal_info
                academic_info.guardian_info = guardian
                academic_info.previous_academic_info = prev_academic_info
                academic_info.previous_academic_certificate = prev_academic_cert
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

@login_required
def student_list_priest(request):
    # Use select_related to prefetch related data
    student = AcademicInfo.objects.select_related('personal_info__user').filter(is_delete=False).order_by('-id')
    context = {'student': student}
    return render(request, 'priest/student_list.html', context)

@login_required
def student_list(request):
    # Use select_related to prefetch related data
    student = AcademicInfo.objects.select_related('personal_info__user').filter(is_delete=False).order_by('-id')
    context = {'student': student}
    return render(request, 'hod/hod_student/student-list.html', context)

@login_required
def student_profile(request, reg_no):
    student = AcademicInfo.objects.get(registration_no=reg_no)
    context = {
        'student': student
    }
    return render(request, 'hod/hod_student/student-profile.html', context)



@login_required
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


@login_required
def student_delete(request, reg_no):
    student = AcademicInfo.objects.get(registration_no=reg_no)
    student.is_delete = True
    student.save()
    return redirect('student-list')


@login_required
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
        return render(request, 'priest/student_serach.html', context)
    else:
        student = AcademicInfo.objects.filter(registration_no=reg_no)
        context = {
            'forms': forms,
            'student': student
        }
        return render(request, 'priest/student_serach.html', context)
    


@login_required
def enrolled_student(request):
    forms = EnrolledStudentForm()
    cls = request.GET.get('class_name', None)
    student = AcademicInfo.objects.filter(class_info=cls, status='not enroll')
    context = {
        'forms': forms,
        'student': student
    }
    return render(request, 'hod/hod_student/enrolled.html', context)


@login_required
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


@login_required
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

#talent programs------------

@never_cache
@login_required(login_url='login_page')
def add_talent_program(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validate the input data
        if not name or not description:
            return render(request, 'talent_program_form.html', {'error': 'Please fill in all fields'})

        # Create a new TalentProgram instance
        TalentProgram.objects.create(name=name, description=description)

        # You can add a success message if needed
        return redirect('talent_program_list')  # Redirect to the list of talent programs or any other appropriate page

    return render(request, 'hod/talent_program/talent_program_form.html')


@login_required(login_url='login_page')
def talent_program_list(request):
    talent_programs = TalentProgram.objects.all()
    return render(request, 'hod/talent_program/talent_program_list.html', {'talent_programs': talent_programs})





from django.shortcuts import render
from .models import TeacherNotice, Notice, EnrolledStudent, TeacherPersonalInfo
@login_required
def teacherdashboard(request):
    latest_notices = TeacherNotice.objects.all().order_by('-date_created')[:5]
    notices = Notice.objects.all().order_by('-date_created')[:5]  # Fetch the latest 5 notices
    enrolled_student = EnrolledStudent.objects.first()

    # Ensure enrolled_student is not None before accessing its ID
    student_id = enrolled_student.id if enrolled_student else None

    teacher = TeacherPersonalInfo.objects.all()
    exam_schedule = ExamSchedule.objects.first()

    # If exam_schedule exists, get its id, otherwise set exam_schedule_id to None
    exam_schedule_id = exam_schedule.id if exam_schedule else None
    context = {
        'teacher': teacher,
        'latest_notices': latest_notices,
        'notices': notices,
        'enrolled_student': enrolled_student,
        'student_id': student_id,  # Add student_id to the context
        'enrolled_student_id': student_id,
        'exam_schedule_id': exam_schedule_id,
          'name':request.user.name  # Add enrolled_student_id to the context
    }
    return render(request, 'teacher/teacher_dashboard.html', context)


@login_required
def staff_take_attendance(request):
    subjects = ClassRegistration.objects.filter(staff_id=request.user.id)
    session_years = Session.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "teacher/attendance/take_attendance.html", context)
 
 


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')
from datetime import date, datetime, timedelta


@login_required
def register_priest(request):
    form = PreistPersonalInfoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            mobile = form.cleaned_data['mobile']
            photo = form.cleaned_data['photo']
            ordination_date = form.cleaned_data['ordination_date']

            # Check if a priest already exists
            existing_priest = PreistPersonalInfo.objects.first()

            # If priest exists, check the ordination date
            if existing_priest:
                three_years_from_ordination = existing_priest.ordination_date + timedelta(days=3*365)  # approximately 3 years
                if datetime.now().date() <= three_years_from_ordination:
                    messages.error(request, 'A priest has already been added. You cannot add another priest for the next 3 years.')
                    return render(request, 'hod/register_priest.html', {'form': form})

            # Check if the email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'A user with this email already exists.')
            else:
                user = CustomUser.objects.create_user(email=email, password=password, name=name, address=address, mobile=mobile, role='priest')
                user.photo = photo
                user.save()

                priest_info = form.save(commit=False)
                priest_info.user = user
                priest_info.save()
                messages.success(request, 'Priest registered successfully!')
                return redirect('hoddashboard')

    context = {'form': form}
    return render(request, 'hod/register_priest.html', context)



@login_required
def view_priests(request):
    priests = PreistPersonalInfo.objects.all()
    context = {
        'priests': priests
    }
    return render(request, 'hod/view_priest.html', context)


@login_required
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
            photo = form.cleaned_data['photo']
            if CustomUser.objects.filter(email=email, role='teacher').exists():
                messages.error(request, 'A teacher with this email already exists.')
            else:
                user = CustomUser.objects.create_user(name=name, email=email, password=password, address=address, mobile=mobile, role='teacher')
                user.photo = photo
                user.save()
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



@login_required
def teacher_list(request):
    teacher = TeacherPersonalInfo.objects.filter(is_delete=False)
  
    context = {'teacher': teacher}
    return render(request, 'hod/teacher-list.html', context)


@login_required
def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)
    context = {
        'teacher': teacher
    }
    return render(request, 'hod/teacher-profile.html', context)


@login_required
def teacher_delete(request, teacher_id):
    teacher = TeacherPersonalInfo.objects.get(id=teacher_id)
    teacher.is_delete = True
    teacher.save()
    return redirect('teacher-list')

@login_required
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



@login_required
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


@login_required
def update_designation(request, designation_id):
    instance = get_object_or_404(Designation, id=designation_id)
    forms = AddDesignationForm(request.POST or None, instance=instance)
    
    if request.method == 'POST':
        if forms.is_valid():
            forms.save()
            return redirect('designation') # Redirect back to the designation page
    
    context = {'forms': forms}
    return render(request, 'hod/designation.html', context)


from django.core.exceptions import ObjectDoesNotExist

#---------------attendance and leaves--------#

from django.contrib.auth.decorators import login_required
@login_required
def mark_attendance(request):
    today = datetime.today().date()

    # Check if today is Sunday
    if today.weekday() != 6:  # 6 represents Sunday in Python's date.weekday() method
        messages.error(request, "Attendance can only be marked on Sundays!")
        return redirect('teacherdashboard')  # Redirect to a suitable page

    # Get the teacher's assigned class
    try:
        guide_teacher = GuideTeacher.objects.get(name=request.user.teacherpersonalinfo)
        assigned_class = guide_teacher.classregistration
    except (GuideTeacher.DoesNotExist, AttributeError):
        print("DEBUG: Teacher is not assigned to any class!") # Debugging line
        messages.error(request, "You are not assigned to any class!")
        return redirect('/')  # Redirect to dashboard or any other suitable page

    # Fetch students of the assigned class
    students = EnrolledStudent.objects.filter(class_name=assigned_class)

    # Get the current session (assuming session name corresponds to the year)
    current_year = datetime.now().year
    print(f"DEBUG: Current year: {current_year}")
    try:
        current_session = Session.objects.get(name=current_year)
    except Session.DoesNotExist:
        print(f"DEBUG: Current session {current_year} not found!") # Debugging line
        messages.error(request, "Current session not found!")
        return redirect('teacherdashboard')  # Redirect to dashboard or any other suitable page

    if request.method == "POST":
        absent_student_ids = request.POST.getlist('absent_students')
    for student in students:
        # Get the ClassInfo instance associated with the class registration of the student
        class_info = student.class_name
        
        # Create a record in the Attendance model
        attendance = Attendance(
            class_info=class_info,
            attendance_date=today,
            session_year_id=current_session
        )
        attendance.save()

        # Create a record in the AttendanceReport model
        is_absent = str(student.id) in absent_student_ids
        AttendanceReport.objects.create(
            student_id=student.student.personal_info,
            attendance_id=attendance,
            status=not is_absent  # True if present, False if absent
        )

    messages.success(request, "Attendance marked successfully!")
    return redirect('mark_attendance')  # Redirect to a suitable page

    return render(request, 'teacher/attendance/mark_attendance.html', {'students': students})

@login_required
def view_class_attendance(request):
    # Get the teacher's assigned class
    try:
        guide_teacher = GuideTeacher.objects.get(name=request.user.teacherpersonalinfo)
        assigned_class = guide_teacher.classregistration
    except (GuideTeacher.DoesNotExist, AttributeError):
        messages.error(request, "You are not assigned to any class!")
        return redirect('/')  # Redirect to dashboard or any other suitable page

    # Fetch students of the assigned class
    students = EnrolledStudent.objects.filter(class_name=assigned_class)
    personal_info_list = [s.student.personal_info for s in students]
    # Fetch attendance records of all students in the assigned class
    attendance_records = AttendanceReport.objects.filter(student_id__in=personal_info_list)

    return render(request, 'teacher/attendance/view_class_attendance.html', {'attendance_records': attendance_records})

@login_required
def view_student_attendance(request):
    # Ensure the user is a student
    if not hasattr(request.user, 'personalinfo'):  # Replace with your student-related attribute check
        messages.error(request, "You are not a student!")
        return redirect('/')  # Redirect to a suitable page

    # Fetch attendance data for the logged-in student
    student_attendance = AttendanceReport.objects.filter(student_id=request.user.personalinfo)

    return render(request, 'student/view_attendance.html', {'attendance_data': student_attendance})



@login_required
def student_leave_view(request):
    if request.method == "POST":
        form = LeaveReportStudentForm(request.POST)
        if form.is_valid():
            try:
                # Assuming the student is logged in and you have access to their object
                student_user = request.user

                # Fetch the corresponding PersonalInfo object for the logged-in user
                student_personal_info = PersonalInfo.objects.get(user=student_user)

                leave_report = form.save(commit=False)
                leave_report.student_id = student_personal_info
                leave_report.save()

                messages.success(request, "Your leave application has been submitted.")
                return redirect('student_leave_view')

            except ObjectDoesNotExist:
                # Handle the error, for example, by displaying an error message
                messages.error(request, "Your personal information is not available. Please ensure it's updated.")
                # No need for the success message here since an error has occurred
                # messages.success(request, "Your leave application has been submitted.")
        # If the form isn't valid, you might want to display an error message, too

    else:
        form = LeaveReportStudentForm()

    leaves = LeaveReportStudent.objects.all()
    context = {
        "form": form,
        "leaves": leaves
    }
    return render(request, 'student/student_leave_view.html', context)

@login_required
def student_leave_approve(request):
    if request.method == "POST":
        # Get the action from the POST data (approve or reject)
        action = request.POST.get('action')
        leave_id = request.POST.get('leave_id')

        # Fetch the leave application by its ID
        leave = LeaveReportStudent.objects.get(id=leave_id)

        if action == "approve":
            leave.leave_status = LeaveReportStudent.APPROVED
            leave.save()
        elif action == "reject":
            leave.leave_status = LeaveReportStudent.REJECTED
            leave.save()
        return redirect('student_leave_approve')  # Redirect back to the same page to see updates

    # Get the list of approved leaves
    approved_leaves = LeaveReportStudent.objects.filter(leave_status=LeaveReportStudent.APPROVED)

    context = {
        "approved_leaves": approved_leaves
    }
    return render(request, 'teacher/attendance/approved_leaves.html', context)

@login_required
def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


@login_required
def teacher_review_leave_applications(request):
    # Fetch all leave applications that are pending
    pending_leaves = LeaveReportStudent.objects.filter(leave_status=LeaveReportStudent.PENDING)
    approved_leaves = LeaveReportStudent.objects.filter(leave_status=LeaveReportStudent.APPROVED)

    if request.method == "POST":
        # Get the action from the POST data (approve or reject)
        action = request.POST.get('action')
        leave_id = request.POST.get('leave_id')

        # Fetch the leave application by its ID
        leave = LeaveReportStudent.objects.get(id=leave_id)

        if action == "approve":
            leave.leave_status = LeaveReportStudent.APPROVED
            leave.save()
        elif action == "reject":
            leave.leave_status = LeaveReportStudent.REJECTED
            leave.save()
        return redirect('teacher_review_leave_applications')  # redirect back to the same page to see updates

    context = {
        "pending_leaves": pending_leaves,
        "approved_leaves": approved_leaves
    }
    return render(request, 'teacher/attendance/teacher_leave_review.html', context)


@login_required
def staff_leave_apply(request):
    staff_user = request.user
    staff_personal_info = TeacherPersonalInfo.objects.get(user=staff_user)
    submitted_leaves = LeaveReportStaff.objects.filter(staff_id=staff_personal_info)
    
    if request.method == "POST":
        form = LeaveReportStaffForm(request.POST)
        if form.is_valid():
            try:                
                leave_report = form.save(commit=False)
                leave_report.staff_id = staff_personal_info
                leave_report.save()

                messages.success(request, "Your leave application has been submitted successfully.")
                return redirect('staff_leave_apply')
            except ObjectDoesNotExist:
                messages.error(request, "Your personal information is not available. Please ensure it's updated.")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = LeaveReportStaffForm()

    context = {
        "form": form,
        "leaves": submitted_leaves
    }

    return render(request, 'teacher/attendance/staff_leave_view.html', context)


@login_required
def admin_review_leaves(request):
    # Fetch all leave applications that are pending
    pending_leaves = LeaveReportStaff.objects.filter(leave_status=LeaveReportStaff.PENDING).select_related('staff_id')

    if request.method == "POST":
        # Get the action from the POST data (approve or reject)
        action = request.POST.get('action')
        leave_id = request.POST.get('leave_id')

        # Fetch the leave application by its ID
        leave = LeaveReportStaff.objects.get(id=leave_id)

        if action == "approve":
            leave.approve()
        elif action == "reject":
            leave.reject()
        return redirect('admin_review_leaves')  # redirect back to the same page to see updates

    # Fetching the classes associated with the teachers
    teacher_classes = {}
    for leave in pending_leaves:
        try:
            assigned_class = ClassRegistration.objects.get(guide_teacher__name=leave.staff_id)
            leave.assigned_class = assigned_class
        except ClassRegistration.DoesNotExist:
            leave.assigned_class = None

    context = {
        "pending_leaves": pending_leaves,
        "teacher_classes": teacher_classes,
    }
    return render(request, 'hod/teacher_leave_review.html', context)


@login_required
def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')
 

@login_required
def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')
 

@login_required
def admin_view_attendance(request):
    subjects = ClassInfo.objects.all()
    session_years = Session.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod/attendance/admin_view_attenndace.html", context)
 
#-------------grade promotion------#


def determine_next_class(student):
    current_class = student.class_name
    current_session = current_class.session
    current_year = datetime.now().year

    next_session_year = current_year + 1
    next_session_name = str(next_session_year)
    
    try:
        next_session = Session.objects.get(name=next_session_name)
    except Session.DoesNotExist:
        return None

    sessions_of_current_year = Session.objects.filter(name=current_year)
    last_session_of_current_year = sessions_of_current_year.latest('date')
    
    if current_session == last_session_of_current_year:
        try:
            next_class = ClassInfo.objects.get(class_name=current_class, session=next_session)
        except ClassInfo.DoesNotExist:
            return None
    else:
        next_class = current_class
    
    return next_class



    

def determine_next_class(student):
    current_class = student.class_name
    current_session = current_class.session
    current_year = datetime.now().year

    next_session_year = current_year + 1
    next_session_name = str(next_session_year)
    
    try:
        next_session = Session.objects.get(name=next_session_name)
    except Session.DoesNotExist:
        return None

    sessions_of_current_year = Session.objects.filter(name=current_year)
    last_session_of_current_year = sessions_of_current_year.latest('date')
    
    if current_session == last_session_of_current_year:
        # Check if the student has completed two academic sessions in the same class
        if student.has_completed_two_sessions_in_same_class():
            try:
                next_class = ClassInfo.objects.get(class_name=current_class, session=next_session)
            except ClassInfo.DoesNotExist:
                return None
        else:
            # If the student hasn't completed two sessions in the same class, remain in the same class
            next_class = current_class
    else:
        next_class = current_class
    
    return next_class

def promote_students(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        
        # Determine the session for the next academic year
        next_academic_year_session = Session.determine_next_academic_year_session()
        
        for student_id in student_ids:
            student = EnrolledStudent.objects.get(id=student_id)
            next_class = determine_next_class(student)  # Ensure this returns ClassInfo
            
            # Ensure next_class is an instance of ClassInfo, not ClassRegistration
            if isinstance(next_class, ClassInfo):
                # Create a new class registration for the next academic year
                ClassRegistration.objects.create(
                    class_name=next_class,
                    section=student.class_name.section,
                    guide_teacher=student.class_name.guide_teacher,
                    session=next_academic_year_session,
                    student=student
                )
                # Mark the student as promoted
                student.promoted = True
                student.save()
            else:
                # Handle the case where next_class is not an instance of ClassInfo
                # You might want to log an error or handle it differently based on your requirements
                pass
        
        messages.success(request, 'Students promoted successfully.')
        return redirect('select_class')
    else:
        return redirect('select_class')


def select_class(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        selected_class = ClassRegistration.objects.get(id=class_id)
        
        # Fetch all students enrolled in the selected class along with their marks and attendance
        students = EnrolledStudent.objects.filter(class_name=selected_class)
        for student in students:
            try:
                student.marks = Mark.objects.get(student=student)
            except Mark.DoesNotExist:
                student.marks = None
            
            student.attendance = Attendance.objects.filter(class_info_id=student.class_name.class_name_id)

        context = {
            'selected_class': selected_class,
            'students': students
        }
        return render(request, 'promotestudent/select_class.html', context)
    else:
        # Handle GET request to render the form for selecting a class
        classes = ClassRegistration.objects.all()
        context = {
            'class_registrations': classes
        }
        return render(request, 'promotestudent/select_class.html', context)



#--------------cicrculars and notfications----#




@login_required
def addNotice(request):    
    if request.user.is_authenticated:
        form=addNoticeform()
        if(request.method=='POST'):
            form=addNoticeform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('display_notices')
        context={'form':form}
        return render(request,'hod/hod_student/circular.html',context)
    else: 
        return redirect('hoddashboard') 


@login_required
def display_notices(request):
    if request.user.is_authenticated:
        notices = Notice.objects.all().order_by('-date_created') # To fetch the latest notices first
       
        context = {'notices': notices}
        return render(request, 'hod/circular_view.html', context)
    else:
        return redirect('hoddashboard')

@login_required    
def update_notice(request, notice_id):
    notice_instance = get_object_or_404(Notice, id=notice_id)

    if request.method == "POST":
        form = addNoticeform(request.POST, instance=notice_instance)
        if form.is_valid():
            form.save()
            return redirect('display_notices')
    else:
        form = addNoticeform(instance=notice_instance)

    context = {
        'form': form,
        'notice': notice_instance
    }
    return render(request, 'hod/hod_student/update_notice.html', context)

        

#------------teacher dashborad---#



@login_required
def class_student(request):
    # Assuming user is logged in and is a GuideTeacher
    try:
        guide_teacher = GuideTeacher.objects.get(name=request.user.teacherpersonalinfo)
    except GuideTeacher.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not a guide teacher!'})

    class_registrations = ClassRegistration.objects.filter(guide_teacher=guide_teacher)
    students = EnrolledStudent.objects.filter(class_name__in=class_registrations)

    context = {
    
        'students': students
    }
    return render(request, 'teacher/class_student.html', context)


@login_required
def add_teacher_notice(request):    
    if request.user.is_authenticated:
        form = TeacherNoticeForm()
        if request.method == 'POST':
            form = TeacherNoticeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('display_teacher_notices')
        context = {'form': form}
        return render(request, 'hod/hod_student/add_notice.html', context)
    else: 
        return redirect('hoddashboard')

@login_required   
def display_teacher_notices(request):
    if request.user.is_authenticated:
        notice = TeacherNotice.objects.all().order_by('-date_created')
        unread_count = Notice.objects.filter(is_read=False).count()
        
        context = {'notice': notice,
                'unread_count': unread_count,}
        return render(request, 'hod/hod_student/notices.html', context)
    else:
        return redirect('hoddashboard')

@login_required    
def add_resource(request):
    # Assuming the teacher is the logged-in user
    teacher = TeacherPersonalInfo.objects.get(user=request.user)
    
    # First, get the GuideTeacher instance for the logged-in teacher
    guide_teacher_instance = GuideTeacher.objects.get(name=teacher)

    # Next, get the ClassRegistration for the guide_teacher_instance
    class_registration = ClassRegistration.objects.get(guide_teacher=guide_teacher_instance)

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)  # Notice the request.FILES added
        if form.is_valid():
            resource = form.save(commit=False)
            resource.teacher_name = teacher
            resource.class_info = class_registration.class_name  # Set the class_info from the ClassRegistration instance
            resource.class_registration = class_registration  # Set the class_registration
            resource.save()  # Now save the model instance
            return redirect('index_resource')
    else:
        form = ResourceForm()
    return render(request, 'teacher/add_resource.html', {'form': form})

from django import template
import os

register = template.Library()

@register.filter(name='basename')
def basename(value):
    return os.path.basename(value)

@login_required
def view_resource():
 return HttpResponseRedirect(reverse('index_resource'))


@login_required
def edit_resource(request, id):  
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




@login_required
def delete_resource(request):
    if request.method == 'POST':
     resource = Resource.objects.get(pk=id)
     resource.delete()
    return HttpResponseRedirect(reverse('index_resource'))


@login_required
def uploadresource(request):
   return render(request,'teacher/resource.html')


@login_required
def index_resource(request):
    # Get the logged-in teacher's resources
    teacher = TeacherPersonalInfo.objects.get(user=request.user)
    resources = Resource.objects.filter(teacher_name=teacher)
    
    return render(request,'teacher/index_resource.html', {'resources': resources})


@login_required(login_url='login_page')
def view_marks(request, student_id):
    
    student = get_object_or_404(EnrolledStudent, id=student_id)

    try:
        guide_teacher = GuideTeacher.objects.get(name=request.user.teacherpersonalinfo)
    except GuideTeacher.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not a guide teacher!'})

    class_registrations = ClassRegistration.objects.filter(guide_teacher=guide_teacher)
    students = EnrolledStudent.objects.filter(class_name__in=class_registrations)

    marks = Mark.objects.filter(student=student)
    
    context = {'student': student, 'marks': marks}
    return render(request, 'teacher/view_mark.html', context)

@login_required(login_url='login_page')
def add_mark(request, student_id):
    student = get_object_or_404(EnrolledStudent, id=student_id)
    
    # Ensure the user is a guide teacher
    if not hasattr(request.user, 'TeacherPersonalInfo'):
        return render(request, 'teacher/error.html', {'message': 'You are not a guide teacher!'})
    
    # Retrieve the guide teacher information
    teacher_personal_info = GuideTeacher.objects.get(name=request.user.TeacherPersonalInfo)

    
    try:
        # Filter class registrations based on the guide teacher
        class_registrations = ClassRegistration.objects.filter(guide_teacher=teacher_personal_info)
        
        # Extract class IDs associated with the guide teacher
        class_ids = class_registrations.values_list('class_name', flat=True)
        
        # Filter students based on the classes associated with the guide teacher
        students = EnrolledStudent.objects.filter(class_name__in=class_ids)
    except ClassRegistration.DoesNotExist:
        students = []  # No students found for this guide teacher
    
    # Check if a mark already exists for the student and class
    existing_mark = Mark.objects.filter(student=student, class_name=student.class_name).first()

    if existing_mark:
        # A mark already exists, redirect to a page indicating that a mark has already been added
        return render(request, 'teacher/mark_already_added.html', {'student': student, 'existing_mark': existing_mark})

    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.student = student
            mark.class_name = student.class_name
            mark.save()
            return redirect(reverse('view_marks', kwargs={'student_id': student_id}))
    else:
        form = MarkForm()

    context = {'form': form, 'students': students, 'student': student}
    return render(request, 'teacher/mark_updation.html', context)



@login_required(login_url='login_page')
def schedule_class(request):
    try:
        guide_teacher = GuideTeacher.objects.get(name=request.user.teacherpersonalinfo)
    except GuideTeacher.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not a guide teacher!'})


    class_registrations = ClassRegistration.objects.filter(guide_teacher=guide_teacher)

    if request.method == 'POST':
        form = ScheduledClassForm(request.POST)
        if form.is_valid():
            # Save the link along with other details
            scheduled_class = form.save(commit=False)
            scheduled_class.link = request.POST.get('link')  # Assuming link is added in the form
            scheduled_class.save()
            return redirect('scheduled_classes')
    else:
        form = ScheduledClassForm()

    # Fetch scheduled classes for the current guide teacher
    scheduled_classes = ScheduledClass.objects.filter(enrolled_class__guide_teacher=guide_teacher)

    context = {
        'form': form,
        'class_registrations': class_registrations,
        'guide_teachers': GuideTeacher.objects.all(),
        'scheduled_classes': scheduled_classes,  # Pass scheduled classes to the template context
    }
    return render(request, 'teacher/schedule_online_class.html', context)


# views.py
@login_required(login_url='login_page')
def scheduled_classes(request):
    try:
        guide_teacher = GuideTeacher.objects.get(name=request.user.teacherpersonalinfo)
    except GuideTeacher.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not a guide teacher!'})

    # Filter scheduled classes based on the classes assigned to the logged-in teacher
    scheduled_classes = ScheduledClass.objects.filter(enrolled_class__guide_teacher=guide_teacher)

    context = {
        'scheduled_classes': scheduled_classes,
    }
    return render(request, 'teacher/scheduled_class.html', context)
    
    # if scheduled_classes.exists():
    #         return render(request, 'teacher/scheduled_classes.html', context)
    # else:
    #         return render(request, 'teacher/no_classes.html')

def delete_scheduled_class(request, scheduled_class_id):
    # Retrieve the scheduled class object
    scheduled_class = get_object_or_404(ScheduledClass, pk=scheduled_class_id)
    
    if request.method == 'POST':
        # Delete the scheduled class
        scheduled_class.delete()
        # Redirect to a success page or another view
        return redirect('scheduled_classes')
    
    # If the request method is not POST, render a confirmation page
    return render(request, 'teacher/delete_scheduled_class.html', {'scheduled_class': scheduled_class})



#-------------priest dashboard----------------------#
@never_cache
@login_required(login_url='login_page')
def priestdashboard(request):
    notices = Notice.objects.all().order_by('-date_created')[:5]  # Fetch the latest 5 notices
    context = {
        
        'notices': notices,
    }
    return render(request,'priest/priestdashboard.html',context)



#--------------studentdashboard-------#


@never_cache
@login_required(login_url='login_page')
def studentdashboard(request):
    notices = Notice.objects.all().order_by('-date_created')[:5]  # Fetch the latest 5 notices
    
    # Fetch the exam schedule for the student (modify this according to your logic)
    exam_schedule = ExamSchedule.objects.first()  # This fetches the first exam schedule, modify as needed
    academic_info = AcademicInfo.objects.all()

    context = {
        'notices': notices,
        'exam_schedule': exam_schedule,
        'academic_info': academic_info,  # Include academic_info in the context
    }
    return render(request, 'student/student_dashboard.html', context)

# def student_resources(request):
#     student_class = EnrolledStudent.objects.get(student__user=request.user).class_name
#     resources = Resource.objects.filter(class_registration=student_class)
#     return render(request, 'student/resources.html', {'resources': resources})


@login_required
def student_resources(request):
    # Fetch the PersonalInfo for the logged-in user.
    personal_info = PersonalInfo.objects.get(user=request.user)
    
    # Fetch the AcademicInfo using the PersonalInfo instance.
    academic_info = AcademicInfo.objects.get(personal_info=personal_info)
    
    # Fetch the EnrolledStudent instance for that AcademicInfo.
    enrolled_student = EnrolledStudent.objects.get(student=academic_info)
    
    # Fetch resources for that class.
    resources = Resource.objects.filter(class_info=enrolled_student.class_name.class_name)
    
    return render(request, 'student/resources.html', {'resources': resources})
from django.http import FileResponse

@never_cache
@login_required
def downloadresource(request, id):
    resource = Resource.objects.get(pk=id)
    file_path = resource.resource_file.path
    response = FileResponse(open(file_path, 'rb'))
    # Additional headers to prompt user download
    response['Content-Disposition'] = f'attachment; filename="{resource.resource_title}"'
    return response

@never_cache
@login_required
def editprofile(request):
   return render(request,'student/edit-profile.html')


@login_required
def online_classes(request):
    # Get the enrolled student based on the logged-in user
    student = EnrolledStudent.objects.get(student__personal_info__user=request.user)

    # Get the scheduled classes for the student's class
    scheduled_classes = ScheduledClass.objects.filter(enrolled_class=student.class_name)

    context = {
        'scheduled_classes': scheduled_classes,
    }

    return render(request, 'student/online_classes.html', context)


@never_cache
@login_required
def attend_class(request, class_id):
    online_class = get_object_or_404(OnlineClass, pk=class_id)
    # Additional logic to check if the student is assigned to the class
    return render(request, 'student/attend_class.html', {'online_class': online_class})
# views.py
@login_required(login_url='login_page')
def view_own_marks(request):
    try:
        student = EnrolledStudent.objects.get(student__personal_info__user=request.user) 
        marks = Mark.objects.filter(student=student)
        context = {'student': student, 'marks': marks}
        return render(request, 'student/view_mark.html', context)
    except EnrolledStudent.DoesNotExist:
        # Handle the case where EnrolledStudent does not exist for the user
        return HttpResponse("EnrolledStudent does not exist for this user.")

@login_required(login_url='login_page')
def request_certificate(request, reg):
    # Assuming the user is logged in
    student = AcademicInfo.objects.get(registration_no=reg)
    

    try:
        # Retrieve the enrolled student information associated with the logged-in user
      enrolled_student = EnrolledStudent.objects.get(student=student)

    except EnrolledStudent.DoesNotExist:
        # Handle the case where the user is not associated with any enrolled student information
        messages.error(request, 'You are not associated with any student account.')
        return redirect('dashboard')  # Redirect to the dashboard or profile page

    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate_request = form.save(commit=False)
            certificate_request.enrolled_student = enrolled_student
            certificate_request.save()

            messages.success(request, 'Certificate request submitted successfully!')
            return redirect('dashboard')  # Redirect to the student's dashboard or profile page
        else:
            messages.error(request, 'Certificate request form is not valid. Please check your inputs.')
    else:
        form = CertificateForm()

    # Get the current class of the enrolled student
    current_class = enrolled_student.class_name

    # Get the list of classes for the dropdown
    available_classes = EnrolledStudent.objects.filter(student__user=student)


    context = {
        'form': form,
        'current_class': current_class,
        'available_classes': available_classes,
    }

    return render(request, 'student/request_certificate.html', context)

#-----register for talent search------#
@login_required(login_url='login_page')
def talent_programs(request):
    programs = TalentProgram.objects.all()
    registrations = Registration.objects.filter(student=request.user)
    existing_registration_ids = [registration.program.id for registration in registrations]

    registration = None  # Initialize registration variable
    success_message = None  # Initialize success message variable

    if request.method == 'POST':
        program_id = request.POST.get('program_id')
        program = TalentProgram.objects.get(id=program_id)

        # Check if the student is already registered for the selected program
        if program.id in existing_registration_ids:
            messages.error(request, 'You are already registered for this program!')
        else:
            # Register the student for the program
            registration = Registration(student=request.user, program=program)
            registration.save()
            success_message = 'Registration successful for {}!'.format(program.name)

    context = {
        'programs': programs,
        'registrations': registrations,
        'registration': registration,  # Include the registration variable in the context
        'success_message': success_message,  # Include the success message in the context
        'existing_registration_ids': existing_registration_ids,  # Include existing registration IDs in the context
    }

    return render(request, 'talentsearch/programs.html', context)


@login_required(login_url='login_page')
def registration_details(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    talent_program = registration.program  # Access the associated TalentProgram
    student = registration.student  # Access the associated student
    return render(request, 'talentsearch/registration_details.html', {
        'registration': registration,
        'talent_program': talent_program,
        'student': student,  # Include the student in the context
    })


#------parent dashboard-----#
from django.shortcuts import render, get_list_or_404, redirect
@never_cache
@login_required(login_url='login_page')
def parentdashboard(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    # Get students related to this guardian (parent).
    students = PersonalInfo.objects.filter(guardian__user=request.user)
    
    # Fetching the IDs of the students.
    student_ids = students.values_list('id', flat=True)
    
    student_attendance = AttendanceReport.objects.filter(student_id__in=student_ids)

    # Fetch resources associated with the students
    student_resources = Resource.objects.filter(class_info__in=student_ids)

    unread_notices = Notice.objects.filter(is_read=False)
    unread_count = unread_notices.count()

    context = {
        'students': students,
        'attendance': student_attendance,
        'student_resources': student_resources,  # Updated variable name
        'unread_count': unread_count,
        'latest_notices': unread_notices[:5]
    }
    return render(request, 'parent/parentdashboard.html', context)


@login_required
def view_student_attendance(request):

    # Check if user is a parent by getting their children
    students = PersonalInfo.objects.filter(guardian__user=request.user)
    if not students.exists():
        messages.error(request, "You are not a parent or no students are associated with your account!")
        return redirect('/')  # Redirect to a suitable page

    # Fetch attendance data for the children
    student_ids = students.values_list('id', flat=True)
    attendance_by_student = {student: AttendanceReport.objects.filter(student_id=student.id) for student in students}

    return render(request, 'parent/viewattendace.html', {'attendance_by_student': attendance_by_student})

@login_required
def view_resources(request):
    # Fetch students associated with the logged-in parent
    students = PersonalInfo.objects.filter(guardian__user=request.user)
    student_ids = students.values_list('id', flat=True)

    # Fetch resources associated with the students
    student_resources = Resource.objects.filter(class_info__in=student_ids)
    
    return render(request, 'parent/downloadresource.html', {'student_resources': student_resources})

@login_required
def download_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    # Check if the user trying to download the resource is indeed the parent of the student the resource is for.
    student = PersonalInfo.objects.filter(guardian__user=request.user, id=resource.class_info_id)
    if not student.exists():
        messages.error(request, "You don't have permission to access this resource.")
        return redirect('parentdashboard')
    
    file_path = resource.resource_file.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{resource.resource_title}"'
    return response

@login_required(login_url='login_page')
def view_student_marks(request):
    try:
        # Get the guardian object associated with the current user
        guardian_info = GuardianInfo.objects.get(user=request.user)
        
        # Retrieve the enrolled students associated with the guardian
        enrolled_students = EnrolledStudent.objects.filter(student__personal_info__guardian=guardian_info)
        
        # Initialize a list to store student marks
        student_marks = []
        
        # Iterate over enrolled students
        for enrolled_student in enrolled_students:
            # Ensure enrolled_student is an instance of EnrolledStudent
            if isinstance(enrolled_student, EnrolledStudent):
                # Retrieve marks for each student
                marks = Mark.objects.filter(student=enrolled_student)
                student_name = enrolled_student.student.personal_info.user.name if enrolled_student.student.personal_info else "Unknown"
                student_marks.append({'student': student_name, 'marks': marks})
        
        # Pass student_marks to the template for rendering
        context = {
            'student_marks': student_marks,
        }
        return render(request, 'parent/student_mark.html', context)
    
    except GuardianInfo.DoesNotExist:
        # Handle the case where GuardianInfo for the user does not exist
        return HttpResponse("GuardianInfo not found for the user.")


    

#-------------student details--------------#
import pandas as pd
from django.http import HttpResponse

def download_student_details(request):
    # Assuming you want to retrieve all students
    students = CustomUser.objects.filter(role='student')

    # Convert student data to a DataFrame
    data = {
        'Name': [student.name for student in students],
        'Email': [student.email for student in students],
        'Mobile': [student.mobile for student in students],
        'Address': [student.address for student in students],
        # Add other fields as needed
    }
    df = pd.DataFrame(data)

    # Create Excel writer object
    writer = pd.ExcelWriter('student_details.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Students')
    writer.save()

    # Prepare response
    excel_file = open('student_details.xlsx', 'rb')
    response = HttpResponse(excel_file.read(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=student_details.xlsx'
    return response
