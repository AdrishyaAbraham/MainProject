
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
from django.contrib import messages
from django.contrib.auth import authenticate, login
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
                elif user.role=='parent':
                    return redirect('parentdashboard')
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


def parent_acprofile(request, parent_id):
    parent_user = get_object_or_404(CustomUser, pk=parent_id, role='parent')
    
    context = {
        'user': parent_user
    }
    
    # Render the template with the context data
    return render(request, 'parent/parentprofile.html', context)

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

    latest_notices = TeacherNotice.objects.all().order_by('-date_created')[:5]
    notices = Notice.objects.all().order_by('-date_created')[:5]  # Fetch the latest 5 notices
    # user=request.user
    # print(user)
    teacher = TeacherPersonalInfo.objects.all()
    context = {
        'teacher': teacher,
        'latest_notices': latest_notices,
        'notices': notices,
    }
    return render(request,'teacher/teacher_dashboard.html',context)

 
def staff_take_attendance(request):
    subjects = ClassRegistration.objects.filter(staff_id=request.user.id)
    session_years = Session.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "teacher/attendance/take_attendance.html", context)
 
 


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
    try:
        current_session = Session.objects.get(name=current_year)
    except Session.DoesNotExist:
        print(f"DEBUG: Current session {current_year} not found!") # Debugging line
        messages.error(request, "Current session not found!")
        return redirect('teacherdashboard')  # Redirect to dashboard or any other suitable page

    if request.method == "POST":
        absent_student_ids = request.POST.getlist('absent_students')
        for student in students:
            student_info = student.student.personal_info  # Moved inside the loop

            # Create a record in the Attendance model
            attendance = Attendance(
                ClassInfo_id=student,
                attendance_date=today,
                session_year_id=current_session
            )
            attendance.save()

            # Create a record in the AttendanceReport model
            is_absent = str(student.id) in absent_student_ids
            AttendanceReport.objects.create(
                student_id=student_info,
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



def student_leave_approve(request):
    
    leave = LeaveReportStudent.objects.get(id=leave_id)
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
        return redirect('student_leave_approve')  # redirect back to the same page to see updates

    context = {
        "approved_leaves": approved_leaves
    }
    return render(request, 'teacher/attendance/approved_leave.html', context)
 
def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')

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

 
def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')
 
 
def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')
 
 
def admin_view_attendance(request):
    subjects = ClassInfo.objects.all()
    session_years = Session.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod/attendance/admin_view_attenndace.html", context)
 
 
#--------------cicrculars and notfications----#

from django.contrib.auth.decorators import login_required


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


def display_notices(request):
    if request.user.is_authenticated:
        notices = Notice.objects.all().order_by('-date_created') # To fetch the latest notices first
       
        context = {'notices': notices}
        return render(request, 'hod/circular_view.html', context)
    else:
        return redirect('hoddashboard')
    
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

def view_resource():
 return HttpResponseRedirect(reverse('index_resource'))

def edit_resource(request, id):  # Add the 'id' argument here
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
    # Get the logged-in teacher's resources
    teacher = TeacherPersonalInfo.objects.get(user=request.user)
    resources = Resource.objects.filter(teacher_name=teacher)
    
    return render(request,'teacher/index_resource.html', {'resources': resources})


#--------------student dashboard-------#
def studentdashboard(request):
    notices = Notice.objects.all().order_by('-date_created')[:5]  # Fetch the latest 5 notices
    context = {
        
        'notices': notices,
    }
    return render(request,'student/student_dashboard.html',context)

# def student_resources(request):
#     student_class = EnrolledStudent.objects.get(student__user=request.user).class_name
#     resources = Resource.objects.filter(class_registration=student_class)
#     return render(request, 'student/resources.html', {'resources': resources})
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

def downloadresource(request, id):
    resource = Resource.objects.get(pk=id)
    file_path = resource.resource_file.path
    response = FileResponse(open(file_path, 'rb'))
    # Additional headers to prompt user download
    response['Content-Disposition'] = f'attachment; filename="{resource.resource_title}"'
    return response

def editprofile(request):
   return render(request,'student/edit-profile.html')


#------parent dashboard-----#
from django.shortcuts import render, get_list_or_404, redirect
@login_required
def parentdashboard(request):
    if not request.user.is_authenticated:
        return redirect('login_page')  # Assuming you have a view called login_page

    # Get students related to this guardian (parent).
    students = PersonalInfo.objects.filter(guardian__user=request.user)
    
    # Fetching the IDs of the students.
    student_ids = students.values_list('id', flat=True)
    
    student_attendance = AttendanceReport.objects.filter(student_id__in=student_ids)

    unread_notices = Notice.objects.filter(is_read=False) # Fetch unread notices
    unread_count = unread_notices.count()

    context = {
        'students': students,
        'attendance': student_attendance,
        'resources': student_resources,  # You need to add a ForeignKey from Resource to PersonalInfo
        'unread_count': unread_count,
        'latest_notices': unread_notices[:5] # display only the 5 latest unread notices
    }

    return render(request, 'parent/parentdashboard.html', context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
