
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
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

def index(request):
    return render(request,'adminpanel/indexdashboard.html')

# def index1(request):
#     return render(request,'adminpanel/index.html',{
#        'students': Student.objects.all()
#     })

# def index2(request):
#     return render(request,'adminpanel/index_teacher.html',{
#        'teachers': Teacher.objects.all()
#     })

# def base(request):
#     return render(request,'adminpanel/base.html')

# def view_student(request, id):
#   return HttpResponseRedirect(reverse('index1'))


# def add(request):
#   if request.method == 'POST':
#     form = StudentForm(request.POST)
#     if form.is_valid():
#       new_student_number = form.cleaned_data['student_number']
#       new_name = form.cleaned_data['name']
#       new_email = form.cleaned_data['email']
      
#       new_student = Student(
#         student_number=new_student_number,
#         name=new_name,
#         email=new_email,
       
#       )
#       new_student.save()
#       return render(request, 'adminpanel/add.html', {
#         'form': StudentForm(),
#         'success': True
#       })
#   else:
#     form = StudentForm()
#   return render(request, 'adminpanel/add.html', {
#     'form': StudentForm()
#   })


# def edit(request, id):
#   if request.method == 'POST':
#     student = Student.objects.get(pk=id)
#     form = StudentForm(request.POST, instance=student)
#     if form.is_valid():
#       form.save()
#       return render(request, 'adminpanel/edit.html', {
#         'form': form,
#         'success': True
#       })
#   else:
#     student = Student.objects.get(pk=id)
#     form = StudentForm(instance=student)
#   return render(request, 'adminpanel/edit.html', {
#     'form': form
#   })


# def delete(request, id):
#   if request.method == 'POST':
#     student = Student.objects.get(pk=id)
#     student.delete()
#   return HttpResponseRedirect(reverse('index1'))

# #teacher----adminpage---


# def base_teacher(request):
#     return render(request,'adminpanel/base_teacher.html')

# def view_teacher(request,id):
#     return HttpResponseRedirect(reverse('index2'))

# def add_teacher(request):
#   if request.method == 'POST':
#     form = TeacherForm(request.POST)
#     if form.is_valid():
#       new_teacher_number = form.cleaned_data['teacher_number']
#       new_name = form.cleaned_data['name']
#       new_email = form.cleaned_data['email']
      
#       new_teacher = Teacher(
#         teacher_number=new_teacher_number,
#         name=new_name,
#         email=new_email,
       
#       )
#       new_teacher.save()
#       return render(request, 'adminpanel/add_teacher.html', {
#         'form': TeacherForm(),
#         'success': True
#       })
#   else:
#     form = TeacherForm()
#   return render(request, 'adminpanel/add_teacher.html', {
#     'form': TeacherForm()
#   })


# def edit_teacher(request, id):
#   if request.method == 'POST':
#     teacher = Teacher.objects.get(pk=id)
#     form = TeacherForm(request.POST, instance=teacher)
#     if form.is_valid():
#       form.save()
#       return render(request, 'adminpanel/edit_teacher.html', {
#         'form': form,
#         'success': True
#       })
#   else:
#     teacher = Teacher.objects.get(pk=id)
#     form = TeacherForm(instance=teacher)
#   return render(request, 'adminpanel/edit_teacher.html', {
#     'form': form
#   })


# def delete_teacher(request, id):
  # if request.method == 'POST':
  #   teacher = Teacher.objects.get(pk=id)
  #   teacher.delete()
  # return HttpResponseRedirect(reverse('index2'))

#----------------HOD-dashboard-----------#

def hoddashboard(request):
   return render(request,'hod/hoddashboard.html')

def index1(request):
    return render(request,'hod/index.html',{
       'students': Student.objects.all()
    })

def index2(request):
    return render(request,'hod/index_teacher.html',{
       'teachers': Teacher.objects.all()
    })

def base(request):
    return render(request,'hod/base.html')

def view_student(request, id):
  return HttpResponseRedirect(reverse('index1'))


def add(request):
  if request.method == 'POST':
    form = StudentForm(request.POST)
    if form.is_valid():
      new_student_number = form.cleaned_data['student_number']
      new_name = form.cleaned_data['name']
      new_email = form.cleaned_data['email']
      new_address=form.cleaned_data['address']
      new_phone_number=form.cleaned_data['phone_number']
      new_gender=form.cleaned_data['gender']
      new_dob=form.cleaned_data['dob']
      new_doj=form.cleaned_data['doj']
      new_fathername=form.cleaned_data['fathername']
      new_father_contact=form.cleaned_data['father_contact']
      new_mothername=form.cleaned_data['mothername']
      new_mother_contact=form.cleaned_data['mother_contact']


      
      new_student = Student(
        student_number=new_student_number,
        name=new_name,
        email=new_email,
        address=new_address,
        phone_number=new_phone_number,
        gener=new_gender,
        dob=new_dob,
        doj=new_doj,
        fathername=new_fathername,
        father_contact=new_father_contact,
        mothername=new_mothername,
        mother_contact=new_mother_contact,

       
      )
      new_student.save()
      return render(request, 'hod/add.html', {
        'form': StudentForm(),
        'success': True
      })
    else:
       print(form.errors)
  else:
     
     form = StudentForm()
  return render(request, 'hod/add.html', {
    'form': StudentForm()
  })


def edit(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
      form.save()
      return render(request, 'hod/edit.html', {
        'form': form,
        'success': True
      })
  else:
    student = Student.objects.get(pk=id)
    form = StudentForm(instance=student)
  return render(request, 'hod/edit.html', {
    'form': form
  })


def delete(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    student.delete()
  return HttpResponseRedirect(reverse('index1'))

def base_teacher(request):
    return render(request,'hod/base_teacher.html')

def view_teacher():
    return HttpResponseRedirect(reverse('index2'))

def add_teacher(request):
  if request.method == 'POST':
    form = TeacherForm(request.POST)
    if form.is_valid():
      new_teacher_number = form.cleaned_data['teacher_number']
      new_name = form.cleaned_data['name']
      new_email = form.cleaned_data['email']
      new_address = form.cleaned_data['address']
      new_phone_number = form.cleaned_data['phone_number']
      new_gender = form.cleaned_data['gender']
      new_dob = form.cleaned_data['dob']
      new_doj = form.cleaned_data['doj']

      
      new_teacher = Teacher(
        teacher_number=new_teacher_number,
        name=new_name,
        email=new_email,
        address=new_address,
        phone_number=new_phone_number,
        gender=new_gender,
        dob=new_dob,
        doj=new_doj,

       
      )
      new_teacher.save()
      return render(request, 'hod/add_teacher.html', {
        'form': TeacherForm(),
        'success': True
      })
  else:
    form = TeacherForm()
  return render(request, 'hod/add_teacher.html', {
    'form': TeacherForm()
  })


def edit_teacher(request, id):
  if request.method == 'POST':
    teacher = Teacher.objects.get(pk=id)
    form = TeacherForm(request.POST, instance=teacher)
    if form.is_valid():
      form.save()
      return render(request, 'hod/edit_teacher.html', {
        'form': form,
        'success': True
      })
  else:
    teacher = Teacher.objects.get(pk=id)
    form = TeacherForm(instance=teacher)
  return render(request, 'hod/edit_teacher.html', {
    'form': form
  })


def delete_teacher(request, id):
  if request.method == 'POST':
    teacher = Teacher.objects.get(pk=id)
    teacher.delete()
  return HttpResponseRedirect(reverse('index2'))

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


def create_section(request):
    forms = SectionForm()
    if request.method == 'POST':
        forms = SectionForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('create-section')
    section = Section.objects.all()
    context = {
        'forms': forms,
        'section': section
    }
    return render(request, 'hod/create_classsection.html', context)  

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
    session = Session.objects.all()
    context = {
        'forms': forms,
        'session': session
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


def load_upazilla(request):
    district_id = request.GET.get('district')
    upazilla = Upazilla.objects.filter(district_id=district_id).order_by('name')

    upazilla_id = request.GET.get('upazilla')
    union = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
    context = {
        'upazilla': upazilla,
        'union': union
    }
    return render(request, 'hod/others/upazilla_dropdown_list_options.html', context)

def load_union(request):
    upazilla_id = request.GET.get('upazilla')
    union = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
    context = {
        'union': union
    }
    return render(request, 'hod/others/union_dropdown_list_options.html', context)


def add_district(request):
    forms = DistrictForm()
    if request.method == 'POST':
        forms = DistrictForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('district')
    district = District.objects.all()
    context = {'forms': forms, 'district': district}
    return render(request, 'hod/address/district.html', context)

def add_upazilla(request):
    forms = UpazillaForm()
    if request.method == 'POST':
        forms = UpazillaForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('upazilla')
    upazilla = Upazilla.objects.all()
    context = {'forms': forms, 'upazilla': upazilla}
    return render(request, 'hod/address/upazilla.html', context)

def add_union(request):
    forms = UnionForm()
    if request.method == 'POST':
        forms = UnionForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('union')
    union = Union.objects.all()
    context = {'forms': forms, 'union': union}
    return render(request, 'hod/address/union.html', context)

def class_wise_student_registration(request):
    register_class = ClassRegistration.objects.all()
    context = {'register_class': register_class}
    return render(request, 'hod/hod_student/class-wise-student-registration.html', context)

def student_registration(request):
    academic_info_form = AcademicInfoForm(request.POST or None)
    personal_info_form = PersonalInfoForm(request.POST or None, request.FILES or None)
    student_address_info_form = StudentAddressInfoForm(request.POST or None)
    guardian_info_form = GuardianInfoForm(request.POST or None)
    emergency_contact_details_form = EmergencyContactDetailsForm(request.POST or None)
    previous_academic_info_form = PreviousAcademicInfoForm(request.POST or None)
    previous_academic_certificate_form = PreviousAcademicCertificateForm(request.POST or None, request.FILES)

    if request.method == 'POST':
        if academic_info_form.is_valid() and personal_info_form.is_valid() and student_address_info_form.is_valid() and guardian_info_form.is_valid() and emergency_contact_details_form.is_valid() and previous_academic_info_form.is_valid() and previous_academic_certificate_form.is_valid():
            s1 = personal_info_form.save()
            s2 = student_address_info_form.save()
            s3 = guardian_info_form.save()
            s4 = emergency_contact_details_form.save()
            s5 = previous_academic_info_form.save()
            s6 = previous_academic_certificate_form.save()
            academic_info = academic_info_form.save(commit=False)
            academic_info.personal_info = s1
            academic_info.address_info = s2
            academic_info.guardian_info = s3
            academic_info.emergency_contact_info = s4
            academic_info.previous_academic_info = s5
            academic_info.previous_academic_certificate = s6
            academic_info.save()
            return redirect('student-list')

    context = {
        'academic_info_form': academic_info_form,
        'personal_info_form': personal_info_form,
        'student_address_info_form': student_address_info_form,
        'guardian_info_form': guardian_info_form,
        'emergency_contact_details_form': emergency_contact_details_form,
        'previous_academic_info_form': previous_academic_info_form,
        'previous_academic_certificate_form': previous_academic_certificate_form
    }
    return render(request, 'hod/hod_student/student-registration.html', context)

def student_list(request):
    student = AcademicInfo.objects.filter(is_delete=False).order_by('-id')
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
    student_address_info_form = StudentAddressInfoForm(instance=student.address_info)
    guardian_info_form = GuardianInfoForm(instance=student.guardian_info)
    emergency_contact_details_form = EmergencyContactDetailsForm(instance=student.emergency_contact_info)
    previous_academic_info_form = PreviousAcademicInfoForm(instance=student.previous_academic_info)
    previous_academic_certificate_form = PreviousAcademicCertificateForm(instance=student.previous_academic_certificate)

    if request.method == 'POST':
        academic_info_form = AcademicInfoForm(request.POST, instance=student)
        personal_info_form = PersonalInfoForm(request.POST, request.FILES, instance=student.personal_info)
        student_address_info_form = StudentAddressInfoForm(request.POST, instance=student.address_info)
        guardian_info_form = GuardianInfoForm(request.POST, instance=student.guardian_info)
        emergency_contact_details_form = EmergencyContactDetailsForm(request.POST, instance=student.emergency_contact_info)
        previous_academic_info_form = PreviousAcademicInfoForm(request.POST, instance=student.previous_academic_info)
        previous_academic_certificate_form = PreviousAcademicCertificateForm(request.POST, request.FILES, instance=student.previous_academic_certificate)
        if academic_info_form.is_valid() and personal_info_form.is_valid() and student_address_info_form.is_valid() and guardian_info_form.is_valid() and emergency_contact_details_form.is_valid() and previous_academic_info_form.is_valid() and previous_academic_certificate_form.is_valid():
            s1 = personal_info_form.save()
            s2 = student_address_info_form.save()
            s3 = guardian_info_form.save()
            s4 = emergency_contact_details_form.save()
            s5 = previous_academic_info_form.save()
            s6 = previous_academic_certificate_form.save()
            academic_info = academic_info_form.save(commit=False)
            academic_info.personal_info = s1
            academic_info.address_info = s2
            academic_info.guardian_info = s3
            academic_info.emergency_contact_info = s4
            academic_info.previous_academic_info = s5
            academic_info.previous_academic_certificate = s6
            academic_info.save()
            return redirect('student-list')

    context = {
        'academic_info_form': academic_info_form,
        'personal_info_form': personal_info_form,
        'student_address_info_form': student_address_info_form,
        'guardian_info_form': guardian_info_form,
        'emergency_contact_details_form': emergency_contact_details_form,
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


  


        
#------------teacher dashborad---#
def teacherdashboard(request):
   return render(request,'teacher/teacher_dashboard.html')

def attendance(request):
   return render(request,'teacher/attendance.html')

def index_resource(request):
   return render(request,'teacher/index_resource.html',{
      'resources':Resource.objects.all()
   })

def add_resource(request):
  if request.method == 'POST':
    form = ResourceForm(request.POST)
    if form.is_valid():
      new_resource_id = form.cleaned_data['resource_id']
      new_resource_title = form.cleaned_data['resource_title']
      new_resource_file = form.cleaned_data['resource_file']
      new_file_type = form.cleaned_data['file_type']
      new_description = form.cleaned_data['description']
      new_uploaded_date = form.cleaned_data['uploaded_date']

      new_resource = Resource(
        resource_id=new_resource_id,
        resource_title=new_resource_title,
        resource_file=new_resource_file,
        file_type=new_file_type,
        description=new_description,
        uploaded_date=new_uploaded_date,
      )
      new_resource.save()
      return render(request, 'teacher/add_resource.html', {
        'form': ResourceForm(),
        'success': True
      })
  else:
    form = ResourceForm()
  return render(request, 'teacher/add_resource.html', {
    'form': ResourceForm()
  })


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




#--------------student dashboard-------#
def studentdashboard(request):
   return render(request,'student/student_dashboard.html')


def downloadresource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    response = FileResponse(resource.resource_file)
    return response

def editprofile(request):
   return render(request,'student/edit-profile.html')

#--------login page and registration-----#
def login_page(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Invalid Login")
            return render(request, 'login/index.html')    

    else:
        return render(request, 'login/index.html')    

def register_page(request):
    if request.method == "POST":
        name = request.POST ['name']
        username = request.POST ['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        phone=request.POST['phone']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                # messages.info(request, 'Username already exists')
                # return redirect('register')
                return render(request, 'login/register.html', {'username_exists': True})
                # if User.objects.filter(userban).exists():
            #     messages.info(request, 'Email already exists') 
            #     return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('')
        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('register')
    else:
        return render(request, 'login/register.html')
    
def logout_user(request):
    print('Logged Out')
    logout(request)
    return redirect('/')